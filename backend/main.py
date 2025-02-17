from example_exercises.kotlin.exercise_1 import exercise_1
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from example_exercises.kotlin.exercise_1 import exercise_1
from agent_trials.multi_agent import MultiAgent


class Features:
    features: list[str]


llm = ChatOpenAI(model="gpt-4o")

if __name__ == "__main__":
    print("== Initialising Agent ==")
    agent = MultiAgent()

    student_code = exercise_1['student_code']
    question = exercise_1['question']
    skel_code = exercise_1['skel_code']

    agent.run({"skel_code": skel_code, "question": question,
              "student_code": student_code})
