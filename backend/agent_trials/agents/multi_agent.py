"""
The second iteration of the multi agent framework introducing more agents to
create a more modular design.


"""
from instances.llm_instance import LLM_instance
from util.types import AttemptContext, FeatureOutput, ExerciseRequirements, IssueConfidenceOutput, ConceptProficiencyModel, CodeComparisonOutput, LearningTrajectory, HintDirective, HintOutput, GraphState
from util.prompts import exercise_requirements_prompt

from setup_db import add_exercise, add_feature_attempt, get_feature_attempts

from langchain_core.messages import HumanMessage
from langgraph.graph import START, END, StateGraph


# == INSTANCES ==
llm = LLM_instance.get_instance()


def exercise_requirement_agent(state: GraphState):
    exercise_text = state['attempt_context'].exercise_text
    skel_code = state['attempt_context'].skel_code
    prompt = exercise_requirements_prompt(
        exercise_text=exercise_text, skel_code=skel_code)

    llm_input = [HumanMessage(content=prompt)]

    requirements: ExerciseRequirements = llm.with_structured_output(
        ExerciseRequirements).invoke(llm_input)

    print(f"\n== requirements ==\n{requirements.exercise_requirements}\n")


class HintEngine:
    def __init__(self):
        # == Build Graph ==
        builder = StateGraph(GraphState)

        # == Add Nodes ==
        builder.add_node("exercise_requirement_agent",
                         exercise_requirement_agent)

        # == Add Edges ==
        builder.add_edge(START, "exercise_requirement_agent")
        builder.add_edge("exercise_requirement_agent", END)

        self.graph = builder.compile()

    def run(self, state: GraphState):
        config = {"configurable": {"thread_id": "1"}}

        graph = self.graph.invoke(state)

        print(graph)
