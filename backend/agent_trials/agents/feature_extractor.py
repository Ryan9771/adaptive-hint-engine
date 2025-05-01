from pydantic import BaseModel
from instances.llm_instance import LLM_instance
from langchain_core.messages import HumanMessage, SystemMessage
from typing_extensions import TypedDict
from langgraph.graph import START, END, StateGraph
from typing import Annotated
import operator
from setup_db import get_feature_attempts, add_feature_attempt, add_exercise, exercise_exists


from types import InputState, OverallState, Features

llm = LLM_instance.get_instance()


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
    Programming Language:
    {language}

    Programming Question:
    {exercise_text}

    Student Code:
    {student_code}
    """

    formatted_input_prompt = input_prompt.format(
        exercise_text=['exercise_text'], student_code=state['student_code'], language=state['language'])

    llm_input = [system_prompt] + \
        [HumanMessage(content=formatted_input_prompt)]

    features: Features = llm.with_structured_output(Features).invoke(llm_input)

    print(f"==== STATE ====\n{state}==== ====")

    return {"current_feature_attempt": features.features}
