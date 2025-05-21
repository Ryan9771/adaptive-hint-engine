from sqlalchemy import create_engine, Column, String, Text, Integer, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict, MutableList
from typing import List

engine = create_engine("sqlite:///store.db", echo=False)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class ExerciseEntry(Base):
    __tablename__ = "exercises"

    exercise_title = Column(String(255), nullable=False)
    exercise_background = Column(Text, nullable=False)
    exercise_key = Column(String(255), primary_key=True)
    exercise_text = Column(Text, nullable=False)
    skel_code = Column(Text, nullable=False)
    language = Column(String(255), nullable=False)

    required_concepts = Column(MutableList.as_mutable(JSON), default=list)

    previous_code = Column(Text, default="")
    student_profile = Column(MutableDict.as_mutable(
        JSON), default=lambda: MutableDict({"concepts": MutableDict()}))
    no_progress_count = Column(Integer, default=0)
    previous_hint = Column(Text, default="")

    def __init__(self, exercise_key, exercise_text, skel_code, language, exercise_title, exercise_background=""):
        """Initialise a question with empty attempts"""
        self.exercise_key = exercise_key
        self.exercise_title = exercise_title
        self.exercise_text = exercise_text
        self.exercise_background = exercise_background
        self.skel_code = skel_code
        self.language = language
        self.previous_code = skel_code
        self.previous_hint = ""

    def set_required_concepts(self, required_concepts: List[str]):
        self.required_concepts = required_concepts
        db_session.add(self)
        db_session.commit()

    def add_feature_attempt(self, feature_list):
        self.feature_attempts.append(feature_list)
        db_session.add(self)
        db_session.commit()

    def _get_exercise_details(self):
        return {
            "exercise_title": self.exercise_title,
            "exercise_text": self.exercise_text,
            "skel_code": self.skel_code,
            "exercise_background": self.exercise_background,
            "previous_code": self.previous_code
        }


def _exercise_exists(exercise_key: str) -> bool:
    """Check if an exercise exists by its key"""
    return db_session.query(ExerciseEntry.exercise_key).filter_by(exercise_key=exercise_key).first() is not None


def _get_exercise(exercise_key):
    """Gets an exercise using the exercise key"""
    exercise = db_session.query(ExerciseEntry).filter_by(
        exercise_key=exercise_key).first()
    if exercise:
        return exercise

    print("=== Exercise not found ===")

    return None


def get_exercise_details(exercise_key: str):
    """Gets the exercise details using the exercise key"""
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        return exercise._get_exercise_details()
    else:
        print("\n=== Exercise doesn't exist ===\n")
        return None


def add_exercise(exercise_key, exercise_background, exercise_text, skel_code, exercise_title, language="python"):
    """
    Adds an exercise to the database with:
        exercise_key: primary key
        exercise_text: The description / question
        skel_code: The skeleton code
    """
    if not _exercise_exists(exercise_key=exercise_key):
        exercise = ExerciseEntry(
            exercise_key, exercise_text, skel_code, language, exercise_title, exercise_background=exercise_background)
        try:
            db_session.add(exercise)
            db_session.commit()
            print(f"Exercise {exercise_key} Added!")
        except Exception as e:
            print(f"\n== Unable to add exercise ==\n{e}")


def delete_exercise(exercise_key: str):
    """Deletes an exercise using the exercise key"""
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        db_session.delete(exercise)
        db_session.commit()
        print(f"Exercise {exercise_key} Deleted!")
    else:
        print("\n=== Exercise doesn't exist ===\n")


def modify_exercise(exercise_key: str, exercise_text="", exercise_background="", skel_code="", exercise_title="", previous_code=""):
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
        if previous_code:
            exercise.previous_code = previous_code

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


def get_no_progress_count(exercise_key: str):
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        return exercise.no_progress_count
    else:
        print("\n=== Exercise doesn't exist ===\n")


def increment_no_progress_count(exercise_key: str):
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        exercise.no_progress_count += 1
        db_session.add(exercise)
        db_session.commit()
    else:
        print("\n=== Exercise doesn't exist ===\n")


def reset_no_progress_count(exercise_key: str):
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        exercise.no_progress_count = 0
        db_session.add(exercise)
        db_session.commit()
    else:
        print("\n=== Exercise doesn't exist ===\n")


def initialise_student_profile(exercise_key: str, concepts: list):
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        exercise.student_profile = MutableDict({"concepts": MutableDict()})

        for concept in concepts:
            exercise.student_profile["concepts"][concept] = MutableDict({
                "scores": MutableList([]),
                "ema": 0.0
            })

        db_session.add(exercise)
        db_session.commit()
    else:
        print("\n=== Exercise doesn't exist ===\n")


def update_student_profile(exercise_key: str, updated_scores: dict = {}, updated_emas: dict = {}):
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        if updated_scores:
            for concept, score in updated_scores.items():
                if concept in exercise.student_profile["concepts"]:
                    exercise.student_profile["concepts"][concept]["scores"].append(
                        score)
                else:
                    exercise.student_profile["concepts"][concept] = MutableDict({
                        "scores": MutableList([score]),
                        "ema": 0
                    })

        if updated_emas:
            for concept, ema in updated_emas.items():
                if concept in exercise.student_profile["concepts"]:
                    exercise.student_profile["concepts"][concept]["ema"] = ema
                else:
                    exercise.student_profile["concepts"][concept] = MutableDict({
                        "scores": MutableList([]),
                        "ema": ema
                    })

        # print(
            # f"\n=== Updated student profile ===\n{exercise.student_profile}\n")

        flag_modified(exercise, "student_profile")
        db_session.commit()


def get_past_concept_scores(exercise_key: str, last_n: int = 5):
    exercise = _get_exercise(exercise_key=exercise_key)
    result = {}

    if exercise:
        student_profile = exercise.student_profile
        # print(f"\n=== Student profile ===\n{student_profile}\n")
        result = {}

        for concept, info in student_profile["concepts"].items():
            result[concept] = info["scores"][-last_n:]
    else:
        print("\n=== Exercise doesn't exist ===\n")

    return result


def get_previous_concept_emas(exercise_key: str):
    exercise = _get_exercise(exercise_key=exercise_key)
    result = {}

    if exercise:
        student_profile = exercise.student_profile
        result = {}

        for concept, info in student_profile["concepts"].items():
            result[concept] = info["ema"]
    else:
        print("\n=== Exercise doesn't exist ===\n")

    return result


def get_previous_code(exercise_key: str):
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        return exercise.previous_code
    else:
        print("\n=== Exercise doesn't exist ===\n")


def set_previous_code(exercise_key: str, previous_code: str):
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        exercise.previous_code = previous_code
        db_session.add(exercise)
        db_session.commit()
    else:
        print("\n=== Exercise doesn't exist ===\n")


def set_previous_hint(exercise_key: str, previous_hint: str):
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        exercise.previous_hint = previous_hint
        db_session.add(exercise)
        db_session.commit()
    else:
        print("\n=== Exercise doesn't exist ===\n")


def get_previous_hint(exercise_key: str):
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        if not exercise.previous_hint:
            return "No previous hint available"
        return exercise.previous_hint
    else:
        print("\n=== Exercise doesn't exist ===\n")


def reset_exercise(exercise_key: str):
    exercise = _get_exercise(exercise_key=exercise_key)

    if exercise:
        exercise.student_profile["concepts"] = MutableDict()
        exercise.previous_hint = ""
        exercise.previous_code = exercise.skel_code
        exercise.no_progress_count = 0
        exercise.required_concepts = MutableList([])
    else:
        print("\n=== Exercise doesn't exist ===\n")

    db_session.commit()


if __name__ == "__main__":
    # Delete the database
    # Base.metadata.drop_all(bind=engine)
    # print(list_all_exercises())
    pass
