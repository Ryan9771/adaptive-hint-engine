from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict


class State(TypedDict):
    student_code_attempt: str
    question: str


def hint_agent(state: State):
    """
    Generates hints simply by looking at the student's attempt and
    the question.
    """
    pass
