from agent_trials.single_agent_cot import SingleHintAgent
from example_exercises.exercise_1 import exercise_1


if __name__ == "__main__":
    print("== Initialising Agent ==")
    agent = SingleHintAgent()
    input_state = exercise_1

    agent.run(state=input_state)
