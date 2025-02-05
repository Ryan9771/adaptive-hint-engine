"""
First iteration of the multi-llm agent system for the hint generation project
"""

from pydantic import BaseModel
from instances.llm_instance import LLM_instance
from langchain_core.messages import HumanMessage, SystemMessage
from typing_extensions import TypedDict
from langgraph.graph import START, END, StateGraph
from typing import Annotated
import operator



# == Define States and Types ==
class Features(BaseModel):
    features: Annotated[list[str], operator.add]


class InputState(TypedDict):
    skel_code: str
    question: str
    student_code: str


class OutputState(TypedDict):
    hint: str


class OverallState(TypedDict):
    skel_code: str
    question: str
    student_code: str
    question_features: Features
    student_code_features: Features
    hint: str


# OpenAI's GPT-4o model
llm = LLM_instance.get_instance()


"""
SKILL / FEATURE AGENT?
- Current features + Current skill from current code
- Previous code features + skill trajectory
- Something to analyse & distinguish
- Something to store
- Something to supply to further nodes on the go without causing overhead
"""

# == Define Nodes ==
def feature_extractor_agent(state: InputState) -> OverallState:
    """
    Extracts key syntax and logical features from the student code
    """
    pass


def skill_progress_tracker_agent(state: OverallState) -> OverallState:
    """
    - Polls from the db for past / current features 

    - Recieves the features from current code. Analyses which concepts are newly 
    introduced or missing. 

    - Notices patterns of struggle vs improvement

    - Receives some sort of notion of time with the metadata of the provided 
    features
    """
    pass


def solution_completeness_evaluator(state: OverallState) -> OverallState:
    """
    Uses the features / code / test cases results to see if there was a 
    compilation error / how much of the student's code is complete -> i.e. 
    whether it satisfies all constraints, whether all the logical components 
    are present or whether its missing key elements
    """
    pass


def data_aggregation_agent(state: OverallState) -> OverallState:
    """
    - Aggregates information from both nodes, structures it and writes to db. 

    - Maybe some sort of flag if the solution is complete
    """
    pass

def hint_generator_agent(state: OverallState) -> OutputState:
    """
    Generates incremental hints based on student's progress and errors. Should 
    tailor the hint according to the skill level of the student
    """
    pass

def feedback_generator_agent(state: OverallState) -> OutputState:
    """
    If the solution is complete, check for redundant operations, optimisation 
    tips etc..
    """
    pass


class MultiAgent:
    def __init__(self):
        # == Build Graph ==
        builder = StateGraph(input=InputState, output=OutputState)

        # == Add Nodes ==

        # == Add Edges ==

        self.graph = builder.compile()

    def run(self, state):
        config = {"configurable": {"thread_id": "1"}}

        for e in self.graph.stream(state, config=config):
            print(e)
