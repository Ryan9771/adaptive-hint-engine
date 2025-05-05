"""
The second iteration of the multi agent framework introducing more agents to
create a more modular design.


"""
from instances.llm_instance import LLM_instance
from util.types import AttemptContext, FeatureOutput, ExerciseRequirements, IssueConfidenceOutput, ConceptProficiencyModel, CodeComparisonOutput, LearningTrajectory, HintDirective, HintOutput, GraphState
from util.prompts import exercise_requirements_prompt

from setup_db import add_exercise, add_feature_attempt, get_feature_attempts, required_concepts_exists, set_required_concepts, get_required_concepts

from langchain_core.messages import HumanMessage
from langgraph.graph import START, END, StateGraph


# == INSTANCES ==
llm = LLM_instance.get_instance()

# == Conditional Edges ==


def decide_exercise_requirements_exists(state: GraphState):
    print("\n== Checking if exercise requirements exist ==\n")

    exercise_key = state['attempt_context'].exercise_key

    if required_concepts_exists(exercise_key=exercise_key):
        return "feature_extractor_agent"

    return "exercise_requirement_agent"

# == Nodes ==


def exercise_requirement_agent(state: GraphState):
    print("\n== Exercise Requirement Agent ==\n")

    exercise_key = state['attempt_context'].exercise_key
    exercise_text = state['attempt_context'].exercise_text
    skel_code = state['attempt_context'].skel_code
    prompt = exercise_requirements_prompt(
        exercise_text=exercise_text, skel_code=skel_code)

    llm_input = [HumanMessage(content=prompt)]

    requirements: ExerciseRequirements = llm.with_structured_output(
        ExerciseRequirements).invoke(llm_input)

    set_required_concepts(
        exercise_key=exercise_key,
        required_concepts=requirements.exercise_requirements
    )

    print(f"\n== requirements ==\n{requirements.exercise_requirements}\n")


def feature_extractor_agent(state: GraphState):
    pass


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

        # == Add Exercise ==
        exercise_key = state['attempt_context'].exercise_key
        exercise_text = state['attempt_context'].exercise_text
        skel_code = state['attempt_context'].skel_code
        language = state['attempt_context'].language
        add_exercise(
            exercise_key=exercise_key,
            exercise_text=exercise_text,
            skel_code=skel_code
        )

        graph = self.graph.invoke(state)

        print(graph)
