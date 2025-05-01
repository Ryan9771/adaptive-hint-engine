from pydantic import BaseModel
from typing import List, Dict


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


class CodeComparisonOutput(BaseModel):
    """Compares the previous and current code implementation to reason about
    the quality of the changes"""
    better_version: str
    reasoning: str
    severity: str


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
