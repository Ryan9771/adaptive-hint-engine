from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, String, Text, Integer
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict, MutableList
from typing import List
from util.types import StudentProfile

engine = create_engine("sqlite:///new-exercise.db", echo=True)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class ExerciseEntry(Base):
    __tablename__ = "exercises"

    exercise_key = Column(String(255), primary_key=True)
    exercise_text = Column(Text, nullable=False)
    skel_code = Column(Text, nullable=False)
    language = Column(String(255), nullable=False)

    required_concepts = Column(MutableList.as_mutable(JSON), default=list)

    student_profile = Column(MutableDict.as_mutable(JSON), default=dict)
    no_progress_count = Column(Integer, default=0)

    def __init__(self, exercise_key, exercise_text, skel_code, language):
        """Initialise a question with empty attempts"""
        self.exercise_key = exercise_key
        self.exercise_text = exercise_text
        self.skel_code = skel_code
        self.language = language

        self.required_concepts = []
        self.feature_attempts = []

        # TODO: migrate to a new table when working with different students
        self.no_progress_count = 0
        self.student_profile = {}

    def set_required_concepts(self, required_concepts: List[str]):
        self.required_concepts = required_concepts
        db_session.add(self)
        db_session.commit()

    def add_feature_attempt(self, feature_list):
        self.feature_attempts.append(feature_list)
        db_session.add(self)
        db_session.commit()


def exercise_exists(exercise_key: str) -> bool:
    """Check if an exercise exists by its key"""
    return db_session.query(ExerciseEntry.exercise_key).filter_by(exercise_key=exercise_key).first() is not None


def add_exercise(exercise_key, exercise_text, skel_code, language):
    """
    Adds an exercise to the database with:
        exercise_key: primary key
        exercise_text: The description / question
        skel_code: The skeleton code
    """
    if not exercise_exists(exercise_key=exercise_key):
        exercise = ExerciseEntry(
            exercise_key, exercise_text, skel_code, language)
        db_session.add(exercise)
        db_session.commit()


def get_exercise(exercise_key):
    """Gets an exercise using the exercise key"""
    exercise = db_session.query(ExerciseEntry).filter_by(
        exercise_key=exercise_key).first()
    if exercise:
        return exercise

    print("=== Exercise no found ===")

    return None


def required_concepts_exists(exercise_key: str) -> bool:
    """Check if an exercise exists by its key"""
    required_concepts = db_session.query(
        ExerciseEntry.required_concepts).filter_by(exercise_key=exercise_key).first()

    return len(required_concepts[0]) > 0


def set_required_concepts(exercise_key: str, required_concepts: List[str]):
    exercise = get_exercise(exercise_key=exercise_key)

    if exercise:
        exercise.set_required_concepts(required_concepts=required_concepts)
    else:
        print("\n=== Exercise doesn't exist ===\n")


def get_required_concepts(exercise_key: str):
    exercise = get_exercise(exercise_key=exercise_key)

    if exercise:
        return exercise.required_concepts
    else:
        print("\n=== Exercise doesn't exist ===\n")


def get_no_progress_count(exercise_key: str):
    exercise = get_exercise(exercise_key=exercise_key)

    if exercise:
        return exercise.no_progress_count
    else:
        print("\n=== Exercise doesn't exist ===\n")


def set_no_progress_count(exercise_key: str, no_progress_count: int):
    exercise = get_exercise(exercise_key=exercise_key)

    if exercise:
        exercise.no_progress_count = no_progress_count
        db_session.add(exercise)
        db_session.commit()
    else:
        print("\n=== Exercise doesn't exist ===\n")


def update_student_profile(exercise_key: str, updated_scores: dict):
    exercise = get_exercise(exercise_key=exercise_key)

    if exercise:
        student_profile = exercise.student_profile
        for concept, score in updated_scores.items():
            if concept in student_profile["concepts"]:
                student_profile["concepts"][concept].append(score)
            else:
                student_profile["concepts"][concept] = [score]
        db_session.add(exercise)
        db_session.commit()


def get_student_profile(exercise_key: str, last_n: int = 5):
    exercise = get_exercise(exercise_key=exercise_key)
    result = {}

    if exercise:
        student_profile = exercise.student_profile
        result = {}

        for concept, scores in student_profile["concepts"].items():
            result[concept] = scores[-last_n:]
    else:
        print("\n=== Exercise doesn't exist ===\n")

    return result


# Delete the database
# Base.metadata.drop_all(bind=engine)
