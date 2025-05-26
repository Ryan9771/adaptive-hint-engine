from sqlalchemy import create_engine, Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict, MutableList
from typing import List
import hashlib

engine = create_engine("sqlite:///store.db", echo=False)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Student(Base):
    """Student db to keep track of per-student progress"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    student_id = Column(String(255), unique=True, nullable=False)

    def __init__(self, name: str):
        self.student_id = self.generate_student_id(name)

    @staticmethod
    def generate_student_id(name: str):
        """Hashes the name to maintain anonymity"""
        return hashlib.sha256(name.encode()).hexdigest()


class ExerciseEntry(Base):
    __tablename__ = "exercises"

    exercise_title = Column(String(255), nullable=False)
    exercise_background = Column(Text, nullable=False)
    exercise_key = Column(String(255), primary_key=True)
    exercise_text = Column(Text, nullable=False)
    skel_code = Column(Text, nullable=False)
    test_cases = Column(Text, nullable=False)
    required_concepts = Column(MutableList.as_mutable(JSON), default=list)

    def __init__(self, exercise_key, exercise_text, skel_code, exercise_title, exercise_background, test_cases):
        """Initialise a question with empty attempts"""
        self.exercise_key = exercise_key
        self.exercise_title = exercise_title
        self.exercise_text = exercise_text
        self.exercise_background = exercise_background
        self.skel_code = skel_code
        self.test_cases = test_cases

    def set_required_concepts(self, required_concepts: List[str]):
        self.required_concepts = required_concepts
        db_session.add(self)
        db_session.commit()

    def _get_exercise_details(self):
        return {
            "exercise_title": self.exercise_title,
            "exercise_text": self.exercise_text,
            "skel_code": self.skel_code,
            "exercise_background": self.exercise_background,
        }


class StudentExercise(Base):
    __tablename__ = "student_exercises"

    id = Column(Integer, primary_key=True)
    student_id = Column(String(255), ForeignKey(
        "students.student_id"), nullable=False)
    exercise_key = Column(String(255), ForeignKey("exercises.exercise_key"))

    previous_code = Column(Text, default="")
    student_profile = Column(MutableDict.as_mutable(
        JSON), default=lambda: MutableDict({"concepts": MutableDict()}))
    attempt_count = Column(Integer, default=0)
    no_progress_count = Column(Integer, default=0)
    previous_hint = Column(Text, default="")
    latest_tone = Column(Text, default="")
    latest_strategy = Column(Text, default="")

    student = relationship("Student", backref="student_exercises")
    exercise = relationship("ExerciseEntry", backref="student_exercises")

    def __init__(self, student_id, exercise_key):
        self.student_id = student_id
        self.exercise_key = exercise_key
        self.previous_hint = ""

        # Set the previous code to the skel code
        exercise = db_session.query(ExerciseEntry).filter_by(
            exercise_key=exercise_key).first()
        if exercise:
            self.previous_code = exercise.skel_code
        else:
            self.previous_code = ""
            print(f"\n== ERROR ==\nExercise {exercise_key} doesn't exist!\n")


def _get_exercise(exercise_key):
    """Gets an exercise using the exercise key"""
    exercise = db_session.query(ExerciseEntry).filter_by(
        exercise_key=exercise_key).first()
    if exercise:
        return exercise

    print("=== Exercise not found ===")

    return None


def get_or_create_student(student_name: str):
    student_id = Student.generate_student_id(student_name)
    student = db_session.query(Student).filter_by(
        student_id=student_id).first()

    if not student:
        student = Student(name=student_name)
        db_session.add(student)
        db_session.commit()
        print(f"New student created with hash {student_id}")

    return student


def get_or_create_exercise(exercise_key, exercise_background="", exercise_text="", skel_code="", exercise_title="", test_cases=""):
    exercise = db_session.query(ExerciseEntry).filter_by(
        exercise_key=exercise_key).first()

    if not exercise:
        exercise = ExerciseEntry(
            exercise_key=exercise_key,
            exercise_background=exercise_background,
            exercise_text=exercise_text,
            skel_code=skel_code,
            exercise_title=exercise_title,
            test_cases=test_cases
        )
        db_session.add(exercise)
        db_session.commit()
        print(f"New exercise created with key {exercise_key}")

    return exercise


def get_or_create_student_exercise(student_name: str, exercise_key: str):
    student = get_or_create_student(student_name=student_name)
    student_id = student.student_id

    student_exercise = db_session.query(StudentExercise).filter_by(
        student_id=student_id, exercise_key=exercise_key).first()

    if not student_exercise:
        student_exercise = StudentExercise(
            student_id=student_id,
            exercise_key=exercise_key
        )

        db_session.add(student_exercise)
        db_session.commit()
        print(f"New student exercise created with key {exercise_key}")

    return student_exercise


def get_exercise_details(student_name: str, exercise_key: str):
    """
    Gets the exercise details using the exercise key and student name.

    Also initialises the student's details if it doesn't exist.
    """
    exercise = get_or_create_exercise(exercise_key=exercise_key)
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )

    if exercise:
        exercise_details = exercise._get_exercise_details()
        # Add the student's latest attempt to the details to load
        #   on the frontend
        exercise_details["previous_code"] = student_exercise.previous_code

        return exercise_details

    print("\n=== Exercise doesn't exist ===\n")
    return None


def delete_exercise(exercise_key: str):
    """Deletes an exercise using the exercise key"""
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        db_session.delete(exercise)
        db_session.commit()
        print(f"Exercise {exercise_key} Deleted!")


def modify_exercise(exercise_key: str, exercise_text="", exercise_background="", skel_code="", exercise_title=""):
    exercise = _get_exercise(exercise_key=exercise_key)
    if exercise:
        if exercise_text:
            exercise.exercise_text = exercise_text
        if exercise_background:
            exercise.exercise_background = exercise_background
        if skel_code:
            exercise.skel_code = skel_code
        if exercise_title:
            exercise.exercise_title = exercise_title

        db_session.commit()
        print("\n== Modified exercise! ==\n")

    else:
        print("\n=== Exercise doesn't exist ===\n")


def list_all_exercises():
    """Lists all exercise titles with their exercise keys"""
    exercises = db_session.query(
        ExerciseEntry.exercise_title, ExerciseEntry.exercise_key).all()
    return [{"title": exercise.exercise_title, "key": exercise.exercise_key} for exercise in exercises]


def required_concepts_exists(exercise_key: str) -> bool:
    """Check if an exercise exists by its key"""
    required_concepts = db_session.query(
        ExerciseEntry.required_concepts).filter_by(exercise_key=exercise_key).first()

    return len(required_concepts[0]) > 0


def set_required_concepts(exercise_key: str, required_concepts: List[str]):
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        exercise.set_required_concepts(required_concepts=required_concepts)
    else:
        print("\n=== Exercise doesn't exist ===\n")


def get_required_concepts(exercise_key: str):
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        return exercise.required_concepts
    else:
        print("\n=== Exercise doesn't exist ===\n")


def get_no_progress_count(student_name: str, exercise_key: str):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )

    if student_exercise:
        return student_exercise.no_progress_count
    else:
        print("\n=== Student Exercise doesn't exist ===\n")


def increment_no_progress_count(student_name: str, exercise_key: str):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )
    if student_exercise:

        student_exercise.no_progress_count += 1
        db_session.add(student_exercise)
        db_session.commit()
    else:
        print("\n=== Student Exercise doesn't exist ===\n")


def reset_no_progress_count(student_name: str, exercise_key: str):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )
    if student_exercise:

        student_exercise.no_progress_count = 0
        db_session.add(student_exercise)
        db_session.commit()
    else:
        print("\n=== Student Exercise doesn't exist ===\n")


def initialise_student_profile(student_name: str, exercise_key: str, concepts: list):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )

    if student_exercise:
        student_exercise.student_profile = MutableDict(
            {"concepts": MutableDict()})

        for concept in concepts:
            student_exercise.student_profile["concepts"][concept] = MutableDict({
                "scores": MutableList([]),
                "ema": 0.0
            })

        db_session.add(student_exercise)
        db_session.commit()
    else:
        print("\n=== Student Exercise doesn't exist ===\n")


def update_student_profile(student_name: str, exercise_key: str, updated_scores: dict = {}, updated_emas: dict = {}, average_ema=0.0):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )

    if student_exercise:
        if updated_scores:
            for concept, score in updated_scores.items():
                if concept in student_exercise.student_profile["concepts"]:
                    student_exercise.student_profile["concepts"][concept]["scores"].append(
                        score)
                else:
                    student_exercise.student_profile["concepts"][concept] = MutableDict({
                        "scores": MutableList([score]),
                        "ema": 0
                    })

        if updated_emas:
            for concept, ema in updated_emas.items():
                if concept in student_exercise.student_profile["concepts"]:
                    student_exercise.student_profile["concepts"][concept]["ema"] = ema
                else:
                    student_exercise.student_profile["concepts"][concept] = MutableDict({
                        "scores": MutableList([]),
                        "ema": ema
                    })

        if average_ema:
            student_exercise.student_profile["concepts"]["average_ema"] = average_ema
        flag_modified(student_exercise, "student_profile")
        db_session.commit()


def get_past_concept_scores(student_name: str, exercise_key: str, last_n: int = 5):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )
    result = {}

    if student_exercise:
        student_profile = student_exercise.student_profile
        result = {}

        for concept, info in student_profile["concepts"].items():
            result[concept] = info["scores"][-last_n:]
    else:
        print("\n=== Student Exercise doesn't exist ===\n")

    return result


def get_previous_code(student_name: str, exercise_key: str):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )

    if student_exercise:
        return student_exercise.previous_code
    else:
        print("\n=== Something went wrong in retrieving the previous code ===\n")


def set_previous_code(student_name: str, exercise_key: str, previous_code: str):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )

    if student_exercise:
        student_exercise.previous_code = previous_code
        db_session.add(student_exercise)
        db_session.commit()
    else:
        print("\n=== Something went wrong in retrieving the previous code ===\n")


def set_previous_hint(student_name: str, exercise_key: str, previous_hint: str):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )

    if student_exercise:
        student_exercise.previous_hint = previous_hint
        db_session.add(student_exercise)
        db_session.commit()
    else:
        print("\n=== Something went wrong in retrieving the previous code ===\n")


def get_previous_hint(student_name: str, exercise_key: str):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )

    if student_exercise:
        if not student_exercise.previous_hint:
            return "No previous hint available"
        return student_exercise.previous_hint
    else:
        print("\n=== Something went wrong in retrieving the previous code ===\n")


def reset_student_exercise(student_name: str):
    student = get_or_create_student(student_name=student_name)
    student_id = student.student_id

    student_exercises = db_session.query(
        StudentExercise).filter_by(student_id=student_id).all()

    if student_exercises:
        for student_exercise in student_exercises:
            exercise = _get_exercise(student_exercise.exercise_key)
            if exercise:
                student_exercise.previous_code = exercise.skel_code
                student_exercise.previous_hint = ""
                student_exercise.no_progress_count = 0
                student_exercise.student_profile = MutableDict(
                    {"concepts": MutableDict()})
            else:
                print(
                    f"\n== Exercise {student_exercise.exercise_key} doesn't exist ==\n")
        db_session.commit()
    else:
        print(f"\n== Exercises of {student_name} not found == \n")


def increment_attempt_count(student_name: str, exercise_key: str):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )
    if student_exercise:
        student_exercise.attempt_count += 1
        db_session.add(student_exercise)
        db_session.commit()
    else:
        print("\n=== Student Exercise doesn't exist ===\n")


def get_attempt_count(student_name: str, exercise_key: str):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )
    if student_exercise:
        return student_exercise.attempt_count
    else:
        print("\n=== Student Exercise doesn't exist ===\n")


def get_evaluation_metrics(student_name: str, exercise_key: str):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )

    concept_emas = {concept: info["ema"] for concept, info in student_exercise.student_profile["concepts"].items(
    ) if concept != "average_ema"}

    if student_exercise:
        return {
            "studentId": student_exercise.student_id,
            "attemptCount": student_exercise.attempt_count,
            "noProgressCount": student_exercise.no_progress_count,
            "averageEma": student_exercise.student_profile["concepts"]["average_ema"],
            "tone": student_exercise.latest_tone,
            "strategy": student_exercise.latest_strategy,
            "conceptEmas": concept_emas
        }


def set_tone_strategy(student_name: str, exercise_key: str, tone: str, strategy: str):
    student_exercise = get_or_create_student_exercise(
        student_name=student_name, exercise_key=exercise_key
    )

    if student_exercise:
        student_exercise.latest_tone = tone
        student_exercise.latest_strategy = strategy
        db_session.add(student_exercise)
        db_session.commit()
    else:
        print("\n=== Something went wrong in setting the tone and strategy ===\n")


if __name__ == "__main__":
    # Delete the database
    # Base.metadata.drop_all(bind=engine)
    # print(list_all_exercises())
    pass
