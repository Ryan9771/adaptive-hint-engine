from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict, MutableList
from typing import List

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
    required_concepts = Column(MutableList.as_mutable(JSON), default=list)
    feature_attempts = Column(MutableList.as_mutable(JSON), default=list)

    def __init__(self, exercise_key, exercise_text, skel_code):
        """Initialise a question with empty attempts"""
        self.exercise_key = exercise_key
        self.exercise_text = exercise_text
        self.skel_code = skel_code
        self.required_concepts = []
        self.feature_attempts = []

    def set_required_concepts(self, required_concepts: List[str]):
        self.required_concepts = required_concepts
        db_session.add(self)
        db_session.commit()

    def add_feature_attempt(self, feature_list):
        """Adds a feature attempt with an incrementing index"""
        self.feature_attempts.append(feature_list)
        db_session.add(self)
        db_session.commit()


def exercise_exists(exercise_key: str) -> bool:
    """Check if an exercise exists by its key"""
    return db_session.query(ExerciseEntry.exercise_key).filter_by(exercise_key=exercise_key).first() is not None


def add_exercise(exercise_key, exercise_text, skel_code):
    """
    Adds an exercise to the database with:
        exercise_key: primary key
        exercise_text: The description / question
        skel_code: The skeleton code
    """
    if not exercise_exists(exercise_key=exercise_key):
        exercise = ExerciseEntry(exercise_key, exercise_text, skel_code)
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


def add_feature_attempt(exercise_key, feature_attempt: list[str]):
    """Adds a list of features of the latest student code attempt"""
    exercise = get_exercise(exercise_key=exercise_key)

    if exercise:
        print("\n== Adding new feature successful ==")
        exercise.add_feature_attempt(feature_attempt)
    else:
        print("\n== Could not add new feature ==")


def get_feature_attempts(exercise_key, last_n=3):
    """Gets the latest n list of features"""
    exercise = get_exercise(exercise_key=exercise_key)

    if exercise:
        return exercise.feature_attempts[-last_n:]

    return None


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


# Delete the database
# Base.metadata.drop_all(bind=engine)
