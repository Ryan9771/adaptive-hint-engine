from pydantic import BaseModel
from instances.llm_instance import LLM_instance
from typing_extensions import TypedDict


# == Define States and Types ==
class Features(BaseModel):
    features: list[str]


# class HintGeneratorOutput(BaseModel):
#     hint: str
#     skill_level


class InputState(TypedDict):
    language: str
    skel_code: str
    exercise_key: str
    exercise_text: str
    student_code: str


class OutputState(TypedDict):
    hint: str
    feedback: str


class OverallState(TypedDict):
    language: str
    skel_code: str
    exercise_key: str
    exercise_text: str
    student_code: str
    current_feature_attempt: Features
    feature_change_analysis: str
    hint: str
    skill_level: str
