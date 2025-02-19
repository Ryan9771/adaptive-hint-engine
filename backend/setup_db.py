from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict

engine = create_engine("sqlite:///exercise.db", echo=True)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class ExerciseEntry(Base):
    __tablename__ = "exercises"

    exercise_key = Column(String(255), primary_key=True)
    exercise_text = Column(Text, nullable=False)
    skel_code = Column(Text, nullable=False)

    # The list of features extracted from student code attempts.
    feature_attempts = Column(MutableDict.as_mutable(JSON), default={})

    def __init__(self, exercise_key, exercise_text, skel_code):
        """Initialise a question with empty attempts"""
        self.exercise_key = exercise_key
        self.exercise_text = exercise_text
        self.skel_code = skel_code
        self.feature_attempts = {}

    def add_feature_attempt(self, feature_list):
        """Adds a feature attempt with an incrementing index"""
        attempt_index = len(self.feature_attempts) + 1
        self.feature_attempts[attempt_index] = feature_list
        db_session.add(self)
        db_session.commit()


def add_exercise(exercise_key, exercise_text, skel_code):
    """
    Adds an exercise to the database with:
        exercise_key: primary key
        exercise_text: The description / question
        skel_code: The skeleton code
    """
    exercise = ExerciseEntry(exercise_key, exercise_text, skel_code)
    db_session.add(exercise)
    db_session.commit()


def get_exercise(exercise_key):
    """Gets an exercise using the exercise key"""
    exercise = db_session.query(ExerciseEntry).filter_by(
        exercise_key=exercise_key).first()
    if exercise:
        return exercise

    return None


def add_feature_attempt(exercise_key, feature_attempt: list[str]):
    """Adds a list of features of the latest student code attempt"""
    exercise = get_exercise(exercise_key=exercise_key)

    if exercise:
        exercise.add_feature_attempt(feature_attempt)


def get_feature_attempts(exercise_key, last_n):
    """Gets the latest n list of features"""
    exercise = get_exercise(exercise_key=exercise_key)

    if exercise:
        all_feature_attempts = exercise.feature_attempts.values()

        return list(all_feature_attempts)[-last_n:]

    return None


# Delete the database
# Base.metadata.drop_all(bind=engine)

# Create the database
Base.metadata.create_all(bind=engine)
