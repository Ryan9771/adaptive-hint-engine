"""
The second iteration of the multi agent framework introducing more agents to 
create a more modular design.


"""
from pydantic import BaseModel
from instances.llm_instance import LLM_instance
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List, Dict, Tuple
from typing_extensions import TypedDict
from langgraph.graph import START, END, StateGraph
from typing import Annotated
import operator
from setup_db import get_feature_attempts, add_feature_attempt, add_exercise, exercise_exists
from types import InputState, OverallState, Features

# == INSTANCES ==
llm = LLM_instance.get_instance()

# === TYPES ===


class AttemptContext(BaseModel):
    """Context from an exercise"""
    exercise_key: str
    exercise_text: str
    skel_code: str
    language: str
    student_code: str


class FeatureOutput(BaseModel):
    """Extracted features from the student's code snippet"""
    included_concepts: str
    missing_concepts: str
    correctness_issues: str
    redundant_concepts: str


class IssueConfidenceOutput(BaseModel):
    """
    Scores how confident an issue is based on the student's attempts on
    a particular exercise
    """
    issues: List[str]
    confidence_scores: Dict[str, float]


class ConceptProficiencyModel(BaseModel):
    """Scores how proficient a student is in each concept for an exercise"""
    concept_proficiency: Dict[str, float]


class LearningTrajectory(BaseModel):
    """
    The trajectory of how the student has progressed based on their past
    attempt of the exercise
    """
    trajectory: str
    changes_summary: str


class HintDirective(BaseModel):
    """Decides the type of hint that should be delivered to the student"""
    strategy: str
    reasoning: str


class HintOutput(BaseModel):
    """The final hint delivered to the student"""
    hint_text: str
