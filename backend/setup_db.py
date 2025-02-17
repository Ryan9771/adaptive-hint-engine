from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///questions.db", echo=True)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class QuestionEntry(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question_text = Column(String(255), nullable=False)
    feature_attempts = Column(JSON, default={})

    def __init__(self, question_text):
        """Initialise a question with empty attempts"""
        self.question_text = question_text
        self.feature_attempts = {}

    def add_feature_attempt(self, feature_list):
        """Adds a feature attempt with an incrementing index"""
        attempt_index = len(self.attempts) + 1
        self.attempts[attempt_index] = feature_list
        db_session.add(self)
        db_session.commit()


Base.metadata.create_all(bind=engine)
