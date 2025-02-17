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


# class HintGeneratorOutput(BaseModel):
#     hint: str
#     skill_level


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
    skill_level: str


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
    hint_generator_prompt = """
    You are an AI hint generator for an introductory programming course, assisting students in solving programming exercises. Your primary goal is to guide students through their learning process without revealing the answer. Instead, you should provide incremental hints tailored to the student's skill level, the current state of their code, and any potential errors they are making.

    You will receive the following input:
        Current Code Snippet: The student's latest attempt at solving the exercise.
        Logical Features: A list of extracted logical and syntactical characteristics of the student's code.
        Exercise Question: A clear problem statement that the student is trying to solve.
        Skeleton Code: The initial code structure provided to the student.
        Skill Level: The estimated proficiency level of the student (e.g., Beginner, Intermediate).

    Your Task:
    - Identify errors or inefficiencies in the student's code by analyzing its logical and syntactical features.
    - Provide an incremental hint that gently guides the student towards the right direction, based on their current understanding and mistakes.
    - Do NOT give away the solution. Instead, offer a nudge that helps them think critically and make the next step independently.

    Adjust the complexity of the hint based on the student's skill level:
    - Beginners may need conceptual guidance, analogies, or hints on syntax.
    - Intermediate students may benefit from questions that prompt them to reconsider their logic.

    Based on all the instructions above, generate as the output, a short and crisp hint for the student
    """
    system_prompt = SystemMessage(content=hint_generator_prompt)

    input_prompt = """
    Current Student Code attempt:
    {student_code}

    Programming question:
    {question}

    Code Features:
    {features}

    Skeleton Code:
    {skel_code}

    Student Skill Level:
    {skill_level}
    """

    formatted_input_prompt = input_prompt.format(
        student_code=state['student_code'], question=state['question'], features=state['features'], skel_code=state['skel_code'], skill_level=state['skill_level'])

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
