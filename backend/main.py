from example_exercises.kotlin.exercise_1 import exercise_1
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
# from example_exercises.kotlin.exercise_1 import exercise_1
from agent_trials.multi_agent import MultiAgent
from example_exercises.python.exercise_1 import exercise_1
from example_exercises.python.exercise_2 import exercise_2
from example_exercises.python.exercise_3 import exercise_3
from example_exercises.python.exercise_4 import exercise_4
from example_exercises.python.exercise_5 import exercise_5

# DB
from setup_db import engine, Base, db_session


class Features:
    features: list[str]


llm = ChatOpenAI(model="gpt-4o")

if __name__ == "__main__":
    # Initialise db
    # Create the database
    Base.metadata.create_all(bind=engine)

    print("== Initialising Agent ==")
    agent = MultiAgent()

    exercise_key = exercise_3["exercise_key"]
    student_code = exercise_3['student_code']
    exercise_text = exercise_3['exercise_text']
    skel_code = exercise_3['skel_code']
    language = exercise_3['language']

    agent.run({"exercise_key": exercise_key, "skel_code": skel_code, "exercise_text": exercise_text,
              "student_code": student_code, "language": language})
