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
    features: list[str]


class InputState(TypedDict):
    skel_code: str
    question: str
    student_code: str


class OutputState(TypedDict):
    hint: str
    feedback: str


class OverallState(TypedDict):
    skel_code: str
    question: str
    student_code: str
    student_code_features: Features
    hint: str


# OpenAI's GPT-4o model
llm = LLM_instance.get_instance()

# == Define Nodes ==


def feature_extractor_agent(state: InputState) -> OverallState:
    """
    Extracts key syntax and logical features from the student code, along 
    with any potential code quality comments
    """
    feature_extractor_prompt = """
    Analyze the given student code for key logical features relevant to the provided programming question. Identify core concepts used (e.g., loops, conditionals, recursion, data structures) and how they relate to solving the problem. Exclude generic syntax details unless they are essential to the solution. Additionally, provide observations on code quality (e.g., redundancy, clarity, structure).

    Return the features as a list of concise strings.

    For example, for a FizzBuzz question, possible extracted features from a student's solution could be:
    ```
    [
        "Uses a for-loop to iterate from 1 to n",
        "Checks divisibility using modulo operator",
        "Correctly prints 'Fizz' for multiples of 3",
        "Correctly prints 'Buzz' for multiples of 5",
        "Handles 'FizzBuzz' case before single conditions",
        "Uses elif to avoid redundant checks",
        "No unnecessary computations or extra conditions"
    ]
    ```
    """
    system_prompt = SystemMessage(content=feature_extractor_prompt)

    input_prompt = """
    Programming Question:
    {question}

    Student Code:
    {student_code}
    """

    formatted_input_prompt = input_prompt.format(
        question=state['question'], student_code=state['student_code'])

    llm_input = [system_prompt] + \
        [HumanMessage(content=formatted_input_prompt)]

    features: Features = llm.with_structured_output(Features).invoke(llm_input)

    return {"student_code_features": features.features}


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


def solution_completeness_evaluator_agent(state: OverallState) -> OverallState:
    """
    Uses the features / code / test cases results to see if there was a 
    compilation error / how much of the student's code is complete -> i.e. 
    whether it satisfies all constraints, whether all the logical components 
    are present or whether its missing key elements
    """
    pass


def data_aggregation_node(state: OverallState) -> OverallState:
    """
    - Aggregates information from both nodes, structures it and writes to db. 

    - Maybe some sort of flag if the solution is complete
    """
    pass


def hint_generator_agent(state: OverallState) -> OutputState:
    """
    Generates incremental hints based on student's progress and errors. Should 
    tailor the hint according to the skill level of the student

    Stores the generated hint into db
    """
    pass


def feedback_generator_agent(state: OverallState) -> OutputState:
    """
    If the solution is complete, check for redundant operations, optimisation 
    tips etc..

    Stores the generated hint into db
    """
    pass


class MultiAgent:
    def __init__(self):
        # == Build Graph ==
        builder = StateGraph(OverallState)

        # == Add Nodes ==
        builder.add_node("feature_extractor_agent", feature_extractor_agent)

        # == Add Edges ==
        builder.add_edge(START, "feature_extractor_agent")
        builder.add_edge("feature_extractor_agent", END)

        self.graph = builder.compile()

    def run(self, state):
        config = {"configurable": {"thread_id": "1"}}

        for e in self.graph.stream(state, config=config):
            print(e)
