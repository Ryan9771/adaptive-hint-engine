"""
The second iteration of the multi agent framework introducing more agents to
create a more modular design.


"""
from instances.llm_instance import LLM_instance
from util.types import AttemptContext, FeatureOutput, ExerciseRequirements, IssueConfidenceOutput, ConceptProficiencyModel, CodeComparisonOutput, LearningTrajectory, HintDirective, HintOutput, GraphState
from util.prompts import exercise_requirements_prompt, feature_extractor_prompt

from setup_db import add_exercise, required_concepts_exists, set_required_concepts, get_required_concepts, get_student_profile, update_student_profile

from langchain_core.messages import HumanMessage
from langgraph.graph import START, END, StateGraph


# == INSTANCES ==
llm = LLM_instance.get_instance()

# == CONSTANTS ==
HISTORY_WINDOW = 5
HISTORY_DECAY = 0.8
MAX_SCORE = 4.0

# == Conditional Edges ==


def decide_exercise_requirements_exists(state: GraphState):
    """Routes to the correct agent based on the existence of
    exercise requirements"""

    print("\n== Checking if exercise requirements exist ==\n")

    exercise_key = state['attempt_context'].exercise_key

    if required_concepts_exists(exercise_key=exercise_key):
        return "feature_extractor_agent"

    return "exercise_requirement_agent"

# == Nodes ==


def exercise_requirement_agent(state: GraphState):
    """Extracts functional requirements from an exercise"""

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

    default_student_profile = {key: []
                               for key in requirements.exercise_requirements}
    update_student_profile(
        exercise_key=exercise_key,
        student_profile=default_student_profile
    )

    print(f"\n== requirements ==\n{requirements.exercise_requirements}\n")


def feature_extractor_agent(state: GraphState):
    """Extracts features from the student code

    Features:
    - included_concepts
    - missing_concepts
    - redundant_concepts
    """
    print("\n== Feature Extractor Agent ==\n")

    exercise_requirements = get_required_concepts(
        exercise_key=state['attempt_context'].exercise_key
    )

    print(f"\n== exercise requirements ==\n{exercise_requirements}\n")

    prompt = feature_extractor_prompt(
        exercise_requirements=exercise_requirements,
        exercise_text=state['attempt_context'].exercise_text,
        skel_code=state['attempt_context'].skel_code,
        student_code=state['attempt_context'].student_code
    )

    llm_input = [HumanMessage(content=prompt)]

    feature_output: FeatureOutput = llm.with_structured_output(
        FeatureOutput).invoke(llm_input)
    print(f"\n== feature output ==\n{feature_output}\n")

    return {"feature_output": feature_output}


def student_profile_agent(state: GraphState):
    """Updates and tracks student proficiency of concepts by maintaining
    a exponential moving average of the scores of the concepts """

    # Get the past concepts scores
    past_concepts_scores = get_student_profile(
        exercise_key=state['attempt_context'].exercise_key,
        last_n=HISTORY_WINDOW
    )

    # Get the concepts the students have implemented
    implemented_concepts = state['feature_output'].implemented_concepts

    # Filter from the past concepts, the scores that are in implemented
    filtered_past_concepts = {
        key: past_concepts_scores[key] for key in implemented_concepts if key in past_concepts_scores}

    ema_build = {}  # Helper dict to build the ema scores
    ema_scores = {}  # The ema scores for the concepts

    # Add the filtered past concepts to the ema_build
    for concept, scores in filtered_past_concepts.items():
        ema_build[concept] = scores

    # Add the current scores to the ema_build
    for concept, score in implemented_concepts.items():
        ema_build[concept].setdefault(concept, []).append(score)

    # Calculate the EMA for each concept
    for concept, scores in ema_build.items():
        ema = scores[0] / 4.0
        for score in scores[1:]:
            ema = (HISTORY_DECAY * ema) + ((1 - HISTORY_DECAY) * score / 4.0)

        ema_scores[concept] = ema

    # for feature_concept in implemented_concepts:
    #     tag = feature_concept.tag
    #     score = feature_concept.score

    pass


def issue_confidence_agent(state: GraphState):
    """Determines which concepts require attention"""
    pass


class HintEngine:
    def __init__(self):
        # == Build Graph ==
        builder = StateGraph(GraphState)

        # == Add Nodes ==
        builder.add_node("exercise_requirement_agent",
                         exercise_requirement_agent)

        builder.add_node("feature_extractor_agent",
                         feature_extractor_agent)

        # == Add Edges ==
        builder.add_conditional_edges(
            START, decide_exercise_requirements_exists
        )

        builder.add_edge("exercise_requirement_agent",
                         "feature_extractor_agent")

        builder.add_edge("feature_extractor_agent", END)

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
            skel_code=skel_code,
            language=language
        )

        graph = self.graph.invoke(state)

        # print(graph)
