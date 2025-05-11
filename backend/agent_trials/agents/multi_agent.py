"""
The second iteration of the multi agent framework introducing more agents to
create a more modular design.


"""
from typing import List, Dict

from instances.llm_instance import LLM_instance
from util.types import (
    AttemptContext,
    FeatureOutput,
    ExerciseRequirements,
    IssueIdentifierOutput,
    StudentProfileOutput,
    CodeComparisonOutput,
    LearningTrajectory,
    HintDirective,
    HintOutput,
    GraphState,
    FeatureDetail
)
from util.prompts import (
    exercise_requirements_prompt,
    feature_extractor_prompt,
    code_comparison_prompt,
)

from setup_db import (
    add_exercise,
    required_concepts_exists,
    set_required_concepts,
    get_required_concepts,
    get_past_concept_scores,
    update_student_profile,
    initialise_student_profile,
    get_previous_code,
    set_previous_code,
    increment_no_progress_count,
    get_no_progress_count,
    reset_no_progress_count
)
from langchain_core.messages import HumanMessage
from langgraph.graph import START, END, StateGraph


# == INSTANCES ==
llm = LLM_instance.get_instance()

# == CONSTANTS ==
HISTORY_WINDOW = 5
HISTORY_DECAY = 0.8
MAX_SCORE = 4.0
STRUGGLE_EMA_THRESHOLD = 0.55
IMPROVE_DELTA = 0.15
MAX_ISSUES = 3
STUCK_ESCALATE = 2
PROFICIENT_THRESHOLD = 0.9

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

    initialise_student_profile(
        exercise_key=exercise_key,
        concepts=requirements.exercise_requirements
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

    print("\n== Student Profile Agent ==\n")

    # Get the past concepts scores
    past_concepts_scores = get_past_concept_scores(
        exercise_key=state['attempt_context'].exercise_key,
        last_n=HISTORY_WINDOW
    )

    print(f"\n== past concepts scores ==\n{past_concepts_scores}\n")

    # Get the concepts the students have implemented
    implemented_concepts: List[FeatureDetail] = state['feature_output'].implemented_concepts

    # Implemented concept scores
    implemented_concepts = {
        concept.tag: concept.score for concept in implemented_concepts
    }

    print(f"\n== implemented concepts ==\n{implemented_concepts}\n")

    # Filter from the past concepts, the scores that are in implemented
    filtered_past_concepts = {
        key: past_concepts_scores[key] for key in implemented_concepts if key in past_concepts_scores
    }

    print(f"\n== filtered past concepts ==\n{filtered_past_concepts}\n")

    ema_build = {}  # Helper dict to build the ema scores
    concept_emas = {}  # The emas for the concepts

    # Add the filtered past concept scores to the ema_build
    for concept, scores in filtered_past_concepts.items():
        ema_build[concept] = scores

    # Add the current scores to the ema_build
    for concept, score in implemented_concepts.items():
        ema_build.setdefault(concept, []).append(score)

    # Calculate the EMA for each concept
    for concept, scores in ema_build.items():
        ema = scores[0] / 4.0
        for score in scores[1:]:
            ema = (HISTORY_DECAY * ema) + ((1 - HISTORY_DECAY) * score / 4.0)

        concept_emas[concept] = round(ema, 2)

    average_ema = sum(concept_emas.values()) / len(concept_emas)

    # Update student profile with new scores
    update_student_profile(
        exercise_key=state['attempt_context'].exercise_key,
        updated_scores=implemented_concepts,
        updated_emas=concept_emas
    )

    # Holds the ema and scores for the implemented concepts
    concept_ema_scores = {concept: {
        "score": implemented_concepts[concept], "ema": concept_emas[concept]} for concept in implemented_concepts}

    print(f"\n== concept ema scores ==\n{concept_ema_scores}\n")

    return {"student_profile_output": StudentProfileOutput(implemented_ema_scores=concept_ema_scores, average_ema=average_ema)}


def issue_identifier_agent(state: GraphState):
    """Determines which concepts require attention"""
    concept_ema_scores = state['student_profile_output'].implemented_ema_scores

    struggling_concepts = []
    improving_concepts = []
    issues = []

    # Compute confidence scores and determine struggling/improving concepts
    for concept, scores in concept_ema_scores.items():
        score = scores["score"]
        ema = scores["ema"]

        # Compute the confidence that the issue is a misconception
        confidence = round(1 - ema, 2)

        if score < MAX_SCORE and ema < STRUGGLE_EMA_THRESHOLD:
            struggling_concepts.append(concept)
        if score / MAX_SCORE > ema + IMPROVE_DELTA:
            improving_concepts.append(concept)

        if score < MAX_SCORE:
            issues.append((concept, confidence))

    # Sort issues based on confidence scores
    issues.sort(key=lambda x: x[1], reverse=True)
    issues = [issue[0] for issue in issues][:MAX_ISSUES]

    issue_identifier_output = IssueIdentifierOutput(
        issues=issues,
        improving_concepts=improving_concepts,
        struggling_concepts=struggling_concepts,
    )

    print(issue_identifier_output)

    return {"issue_identifier_output": issue_identifier_output}


def code_comparison_agent(state: GraphState):
    """Compares the student's previous and current code versions to 
    determine the quality of changes made"""
    print("\n== Code Comparison Agent ==\n")

    previous_code = get_previous_code(
        exercise_key=state['attempt_context'].exercise_key
    )
    current_code = state['attempt_context'].student_code
    prompt = code_comparison_prompt(
        exercise_text=state['attempt_context'].exercise_text,
        previous_code=previous_code,
        current_code=current_code
    )

    llm_input = [HumanMessage(content=prompt)]
    code_comparison_output: CodeComparisonOutput = llm.with_structured_output(
        CodeComparisonOutput).invoke(llm_input)
    print(f"\n== code comparison output ==\n{code_comparison_output}\n")

    set_previous_code(
        exercise_key=state['attempt_context'].exercise_key,
        previous_code=state['attempt_context'].student_code
    )

    # Update the no progress count if the logic is identical
    if code_comparison_output.identical_logic == "true":
        increment_no_progress_count(
            exercise_key=state['attempt_context'].exercise_key
        )
    else:
        reset_no_progress_count(
            exercise_key=state['attempt_context'].exercise_key
        )

    return {"code_comparison_output": code_comparison_output}


def hint_directive_agent(state: GraphState):
    """Decides the tonality and the type of hint to deliver"""
    print("\n== Hint Directive Agent ==\n")

    stuck_count = get_no_progress_count(
        exercise_key=state['attempt_context'].exercise_key
    )

    print(f"\n== stuck count ==\n{stuck_count}\n")

    average_ema = state['student_profile_output'].average_ema
    feature_output = state['feature_output']
    issue_identifier_output = state['issue_identifier_output']

    # Natural language directives
    tone = "clear"
    strategy = ""
    rationale = ""

    # Set the tone based on whether the student is stuck or struggling
    if stuck_count > STUCK_ESCALATE and average_ema < STRUGGLE_EMA_THRESHOLD:
        tone = "beginner-friendly"
        rationale = "Student is stuck and struggling. A short parallel example will help. "
    elif stuck_count > STUCK_ESCALATE:
        tone = "beginner-friendly"
        rationale = "Student is stuck. A conceptual hint will help. "
    elif average_ema < STRUGGLE_EMA_THRESHOLD:
        tone = "clear"
    elif average_ema > PROFICIENT_THRESHOLD:
        tone = "technical"
        rationale = "Student is overally proficient. Perhaps a question to prompt deeper thinking. "

    # Gather issues and their details
    issue_details: Dict[str, str] = {}

    # severity-3 redundancies have priority
    for red in feature_output.redundant_concepts:
        if red.severity == 3:
            issue_details[red.concept] = red.detail

    # add the top conceptual issues
    for issue in issue_identifier_output.issues:
        for fd in feature_output.implemented_concepts:
            if fd.tag == issue and fd.detail:
                issue_details[issue] = fd.detail
                break

    # Specify the issues
    if issue_identifier_output.issues:
        strategy = "conceptual"
        rationale += "Issues Based on Importance:\n" + "\n".join(
            [f"{concept} - {detail}" for concept,
                detail in list(issue_details.items())[:MAX_ISSUES]]
        )
    elif feature_output.missing_concepts:
        strategy = "next_step"
        rationale += "Missing concepts:\n" + \
            ", ".join(feature_output.missing_concepts[:MAX_ISSUES])
    elif feature_output.redundant_concepts:
        strategy = "cleanup"
        rationale += f"Redundant concepts: {[f"{red.concept} - {red.detail}" for red in feature_output.redundant_concepts[:MAX_ISSUES]]}"
    else:
        print(f"\n== Fallback case where no issues / redundancies / missing_concepts detected ==\n")
        strategy = "reflective"
        rationale += "No issues detected. Encourage self-reflection."

    return {
        "hint_directive": HintDirective(
            strategy=strategy,
            rationale=rationale,
            tone=tone
        )
    }


class HintEngine:
    def __init__(self):
        # == Build Graph ==
        builder = StateGraph(GraphState)

        # == Add Nodes ==
        builder.add_node("exercise_requirement_agent",
                         exercise_requirement_agent)

        builder.add_node("feature_extractor_agent",
                         feature_extractor_agent)

        builder.add_node("student_profile_agent", student_profile_agent)

        builder.add_node("issue_identifier_agent", issue_identifier_agent)

        builder.add_node("code_comparison_agent", code_comparison_agent)

        # == Add Edges ==
        builder.add_conditional_edges(
            START, decide_exercise_requirements_exists
        )

        builder.add_edge("exercise_requirement_agent",
                         "feature_extractor_agent")

        builder.add_edge("feature_extractor_agent", "student_profile_agent")

        builder.add_edge("student_profile_agent", "issue_identifier_agent")

        builder.add_edge("issue_identifier_agent", "code_comparison_agent")

        builder.add_edge("code_comparison_agent", END)

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
