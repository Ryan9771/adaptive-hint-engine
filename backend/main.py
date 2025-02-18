from example_exercises.kotlin.exercise_1 import exercise_1
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from example_exercises.kotlin.exercise_1 import exercise_1
from agent_trials.multi_agent import MultiAgent
from setup_db import db_session, ExerciseEntry, add_exercise, get_exercise, add_feature_attempt, get_feature_attempts

# Kotlin Exercise 1

student_code = exercise_1['student_code']
question = exercise_1['question']
skel_code = exercise_1['skel_code']
exercise_1_key = "kotlin_exercise_1"

exercise = ExerciseEntry(exercise_key=exercise_1_key,
                         exercise_text=question, skel_code=skel_code)

three_sample_feature_attempts = [
    ["syntax_error", "missing_colon", "runtime_error", "undeclared_variable"],
    ["incorrect_logic", "off_by_one_error",
        "hardcoded_values", "missing_modulo_check"],
    ["inefficient_loop", "unnecessary_conditionals",
        "repetitive_code", "poor_variable_naming"]
]

map(lambda xs: add_feature_attempt(exercise_key=exercise_1_key,
    feature_attempt=xs), three_sample_feature_attempts)


print(get_feature_attempts(exercise_key=exercise_1_key, last_n=3))

# == Agent Run Attempt ==

# class Features:
#     features: list[str]


# llm = ChatOpenAI(model="gpt-4o")

# if __name__ == "__main__":
#     print("== Initialising Agent ==")
#     agent = MultiAgent()

#     student_code = exercise_1['student_code']
#     question = exercise_1['question']
#     skel_code = exercise_1['skel_code']

#     agent.run({"skel_code": skel_code, "question": question,
#               "student_code": student_code})
