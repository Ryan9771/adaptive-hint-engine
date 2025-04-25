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
from setup_db import get_feature_attempts, add_feature_attempt, add_exercise, exercise_exists


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


class SkillProgressOutput(BaseModel):
    analysis: str
    skill_level: str


def skill_progress_tracker_agent(state: OverallState) -> OverallState:
    """
    - Polls from the db for past features 

    - Recieves the features from current code. Analyses which concepts are newly 
    introduced or missing. 

    - Notices patterns of struggle vs improvement

    - Receives some sort of notion of time with the metadata of the provided 
    features
    """

    feature_prompt = """
    You are an expert programming instructor tasked with analyzing a student's coding progress. You will receive:

    1. A list of lists containing features from the student's past code attempts.
    2. A list of features from the student's current code attempt.
    3. The programming question the student is trying to solve.

    Your task is to:

    1. Analyze the patterns and differences between the past attempts and the current attempt (if there are any past attempts, else use the skeleton code).
    2. Evaluate the student's trajectory and determine if they are on the right path to solve the question.
    3. Provide a concise description of the changes the student has made compared to the last attempt (if applicable, otherwise compare it to the skeleton code).
    4. Assess whether previous attempts were better and specify which one(s), if applicable.

    Your analysis should be brief and aimed at helping a teacher understand the student's progress. The output will be used to generate a hint for the student, so focus on key insights that can guide their learning.

    Please format your response as follows:

    1. Trajectory: [Brief assessment of whether the student is on the right path]
    2. Changes: [Concise description of main changes in the current attempt]
    3. Comparison: [Brief evaluation of current attempt vs. previous attempts]
    4. Key Insights: [1-2 sentences highlighting the most important observations]
    5. Determine the user's programming proficiency as either “low,” “medium,” or “high,” and store it in the skill_level variable. Use this classification to guide the teacher in adjusting the hint's complexity.

    Programming Language:
    {language}

    Programming Question: 
    {exercise_text}

    Past Attempts Features:
    {formatted_past_attempts} 

    Current Attempt Features:
    {current_feature_attempt}

    Skeleton Code:
    {skel_code}

    Analyze the provided information and generate your response based on the format above.
    """

    if exercise_exists(state['exercise_key']):
        past_feature_attempts = get_feature_attempts(
            exercise_key=state['exercise_key'], last_n=2)
        if past_feature_attempts:
            # Format the previous features
            formatted_attempts = []
            num_attempts = len(past_feature_attempts)

            for i, attempt in enumerate(past_feature_attempts):
                attempt_num = num_attempts - i  # Convert index to "n attempts ago"
                formatted_attempts.append(
                    f"{attempt_num} attempt{'s' if attempt_num > 1 else ''} ago:")
                formatted_attempts.extend(
                    f"- {feature}" for feature in attempt)
                formatted_attempts.append("")  # Add a newline for spacing

            formatted_past_attempts = "\n".join(formatted_attempts).strip()
    else:
        add_exercise(state['exercise_key'],
                     state['exercise_text'], state['skel_code'])
        formatted_past_attempts = ""

    print(
        f"\n===== PAST FEATURE ATTEMPTS =====\n{formatted_past_attempts}\n===== =====")

    # Format current feature attempt
    curr_formatted_attempt = []
    curr_formatted_attempt.append(
        "\n".join(state['current_feature_attempt']).strip())

    # Format the prompt
    formatted_prompt = feature_prompt.format(
        language=state['language'],
        exercise_text=state['exercise_text'],
        formatted_past_attempts=formatted_past_attempts,
        current_feature_attempt=curr_formatted_attempt,
        skel_code=state['skel_code']
    )

    skill_progress_output = llm.with_structured_output(
        SkillProgressOutput).invoke([HumanMessage(content=formatted_prompt)])

    feature_change_analysis = skill_progress_output.analysis
    skill_level = skill_progress_output.skill_level

    print(
        f"Skill Progress Output: {feature_change_analysis}\nSkill Level: {skill_level}")

    # Push the current features to db
    add_feature_attempt(state["exercise_key"],
                        state['current_feature_attempt'])

    return {"feature_change_analysis": feature_change_analysis, "skill_level": skill_level}


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
        Past vs current code features analysis: An analysis of what code feature changes have been made from previous attempts of the student 
        Exercise Question: A clear problem statement that the student is trying to solve.
        Skeleton Code: The initial code structure provided to the student.
        Skill Level: The estimated proficiency level of the student (e.g., low, medium, high).
        

    Your Task:
    - Identify errors or inefficiencies in the student's code by analyzing its logical and syntactical features.
    - Provide an incremental hint that gently guides the student towards the right direction, based on their current understanding and mistakes.
    - Do NOT give away the solution. Instead, offer a nudge that helps them think critically and make the next step independently.

    Adjust the complexity of the hint based on the student's skill level:
    - Beginners may need conceptual guidance, analogies, or hints on syntax. Though remember, this should only be the NEXT STEP hint, not a brief hint for solving the entire question at one go.
    - Intermediate students may benefit from questions that prompt them to reconsider their logic.

    Based on all the instructions above, generate as the output, a short and crisp hint for the student
    """
    system_prompt = SystemMessage(content=hint_generator_prompt)

    input_prompt = """
    Programming Language:
    {language}

    Past Vs current Code features analysis:
    {feature_change_analysis}

    Current Student Code attempt:
    {student_code}

    Programming question:
    {exercise_text}

    Skeleton Code:
    {skel_code}

    Student Skill Level:
    {skill_level}
    """

    formatted_input_prompt = input_prompt.format(
        language=state['language'],
        feature_change_analysis=state['feature_change_analysis'],
        student_code=state['student_code'],
        exercise_text=state['exercise_text'],
        skel_code=state['skel_code'],
        skill_level=state['skill_level']
    )
    llm_input = [system_prompt] + \
        [HumanMessage(content=formatted_input_prompt)]

    hint = llm.invoke(llm_input)

    return {"hint": hint.content}


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
        builder.add_node("skill_progress_tracker_agent",
                         skill_progress_tracker_agent)
        builder.add_node("hint_generator_agent", hint_generator_agent)

        # == Add Edges ==
        builder.add_edge(START, "feature_extractor_agent")
        builder.add_edge("feature_extractor_agent",
                         "skill_progress_tracker_agent")
        builder.add_edge("skill_progress_tracker_agent",
                         "hint_generator_agent")
        builder.add_edge("hint_generator_agent", END)

        self.graph = builder.compile()

    def run(self, state):
        config = {"configurable": {"thread_id": "1"}}

        for e in self.graph.stream(state, config=config):
            print(e)
