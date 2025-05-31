from pydantic import BaseModel
from typing import List, Dict, Optional, Union, Tuple
from typing_extensions import TypedDict


class AttemptContext(BaseModel):
    """Context from an exercise"""
    student_name: str
    exercise_key: str
    exercise_text: str
    skel_code: str
    student_code: str
    error: str
    test_results: str


class FeatureDetail(BaseModel):
    def __str__(self):
        return f"tag: {self.tag}\n\t\tscore: {self.score}\n\t\tdetail: {self.detail}\n"
    tag: str
    score: int
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
    """
    {
        "concept_name": {
            "scores": [1, 3, 4],
            "ema": 0.75
        }
    } 
    """
    concepts: Dict[str, Dict[str, Union[List[float], float]]]


class IssueIdentifierOutput(BaseModel):
    """
    Scores how confident an issue is based on the student's attempts on
    a particular exercise
    """

    def __str__(self):
        return f"\n== Issue Identifier Output ==\n" + \
            f"issues: {self.issues}\n" + \
            f"improving_concepts: {self.improving_concepts}\n" + \
            f"struggling_concepts: {self.struggling_concepts}\n"

    issues: List[str]
    improving_concepts: List[str]
    struggling_concepts: List[str]


class StudentProfileOutput(BaseModel):
    """Scores how proficient a student is in each concept for an exercise"""
    implemented_ema_scores: Dict[str, Dict[str, Union[int, float]]]
    average_ema: float


class CodeComparisonOutput(BaseModel):
    """Compares the previous and current code implementation to reason about
    the quality of the changes"""
    identical_logic: str
    change_quality: str
    reasoning: str


class HintDirective(BaseModel):
    """Decides the type of hint that should be delivered to the student"""
    strategy: str
    rationale: str
    tone: str


class HintOutput(BaseModel):
    """The final hint delivered to the student"""
    hint_text: str


class GraphState(TypedDict):
    attempt_context: AttemptContext
    feature_output: FeatureOutput
    num_exercise_requirements: int
    issue_identifier_output: IssueIdentifierOutput
    student_profile_output: StudentProfileOutput
    code_comparison_output: CodeComparisonOutput
    hint_directive: HintDirective
    hint_output: HintOutput


class SimpleGraphState(TypedDict):
    skel_code: str
    exercise_text: str
    student_code: str
    hint: str
    error: str
    test_results: str
