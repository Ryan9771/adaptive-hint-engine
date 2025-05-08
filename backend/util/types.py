from pydantic import BaseModel
from typing import List, Dict, Optional
from typing_extensions import TypedDict


class AttemptContext(BaseModel):
    """Context from an exercise"""
    exercise_key: str
    exercise_text: str
    skel_code: str
    language: str
    student_code: str


class FeatureDetail(BaseModel):
    def __str__(self):
        return f"tag: {self.tag}\n\t\tscore: {self.score}\n\t\tdetail: {self.detail}\n"
    raw_tag: str
    score: int
    tag: str
    detail: Optional[str]


class RedunantConcepts(BaseModel):
    def __str__(self):
        return f"concept: {self.concept}\n\t\tseverity: {self.severity}\n\t\tdetail: {self.detail}"
    concept: str
    severity: int
    detail: str


class FeatureOutput(BaseModel):
    """Extracted features from the student's code snippet"""

    def __str__(self):
        return (
            f"implemented_concepts: [\n\t" +
            "\n\t".join(str(c) for c in self.implemented_concepts) +
            f"\n]\nmissing_concepts: {self.missing_concepts}" +
            f"\nredundant_concepts: [\n\t" +
            "\n\t".join(str(c) for c in self.redundant_concepts) + "\n]"
        )

    implemented_concepts: List[FeatureDetail]
    missing_concepts: List[str]
    redundant_concepts: List[RedunantConcepts]


class ExerciseRequirements(BaseModel):
    exercise_requirements: List[str]


class StudentProfile(BaseModel):
    concepts: Dict[str, List[float]]


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


class GraphState(TypedDict):
    attempt_context: AttemptContext
    feature_output: FeatureOutput
    issue_confidence_output: IssueConfidenceOutput
    concept_proficiency_model: ConceptProficiencyModel
    code_comparison_ouput: CodeComparisonOutput
    learning_trajectory: LearningTrajectory
    hint_directive: HintDirective
    hint_output: HintOutput
