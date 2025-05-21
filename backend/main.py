from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from util.types import AttemptContext
from agent_trials.agents.multi_agent import HintEngine
from example_exercises.python.exercise_1 import exercise_1
from example_exercises.python.exercise_2 import exercise_2
from example_exercises.python.exercise_3 import exercise_3
from example_exercises.python.exercise_4 import exercise_4
from example_exercises.python.exercise_5 import exercise_5

# DB
from db.setup_db import engine, Base


class Features:
    features: list[str]


llm = ChatOpenAI(model="gpt-4o")

if __name__ == "__main__":
    # Initialise db
    # Create the database
    Base.metadata.create_all(bind=engine)

    # print("== Initialising Agent ==")
    # agent = HintEngine()

    # exercise_key = exercise_2["exercise_key"]
    # student_code = exercise_2['student_code']
    # exercise_text = exercise_2['exercise_text']
    # skel_code = exercise_2['skel_code']
    # language = exercise_2['language']

    # attempt_context: AttemptContext = AttemptContext(
    #     exercise_key=exercise_key,
    #     exercise_text=exercise_text,
    #     skel_code=skel_code,
    #     language=language,
    #     student_code=student_code
    # )

    # agent.run({"attempt_context": attempt_context})
