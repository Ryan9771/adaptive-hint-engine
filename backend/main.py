from example_exercises.kotlin.exercise_1 import exercise_1
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
# from example_exercises.kotlin.exercise_1 import exercise_1
from agent_trials.multi_agent import MultiAgent
from setup_db import add_exercise, get_exercise, add_feature_attempt, get_feature_attempts
from example_exercises.python.exercise_1 import exercise_1


class Features:
    features: list[str]


llm = ChatOpenAI(model="gpt-4o")

if __name__ == "__main__":
    print("== Initialising Agent ==")
    agent = MultiAgent()

    exercise_key = exercise_1["exercise_key"]
    student_code = exercise_1['student_code']
    exercise_text = exercise_1['exercise_text']
    skel_code = exercise_1['skel_code']
    language = exercise_1['language']

    agent.run({"exercise_key": exercise_key, "skel_code": skel_code, "exercise_text": exercise_text,
              "student_code": student_code, "language": language})
