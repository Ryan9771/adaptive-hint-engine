"""
The second iteration of the multi agent framework introducing more agents to
create a more modular design.


"""
from typing import List, Dict

from instances.llm_instance import LLM_instance
from util.types import (
    FeatureOutput,
    ExerciseRequirements,
    IssueIdentifierOutput,
    StudentProfileOutput,
    CodeComparisonOutput,
    HintDirective,
    HintOutput,
    GraphState,
    FeatureDetail
)
from util.prompts import (
    exercise_requirements_prompt,
    feature_extractor_prompt,
    code_comparison_prompt,
    hint_generator_prompt
)

from db.setup_db import (
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
    reset_no_progress_count,
    get_previous_hint,
    set_previous_hint,
    increment_attempt_count
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
STUCK_ESCALATE = 1
STUCK_DECAY = 0.6
PROFICIENT_THRESHOLD = 0.9
HIGH_CONCEPT_COVERAGE = 0.8

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
        student_name=state['attempt_context'].student_name,
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

    # print(f"\n== exercise requirements ==\n{exercise_requirements}\n")

    prompt = feature_extractor_prompt(
        exercise_requirements=exercise_requirements,
        exercise_text=state['attempt_context'].exercise_text,
        skel_code=state['attempt_context'].skel_code,
        student_code=state['attempt_context'].student_code
    )

    llm_input = [HumanMessage(content=prompt)]

    feature_output: FeatureOutput = llm.with_structured_output(
        FeatureOutput).invoke(llm_input)

    increment_attempt_count(
        student_name=state['attempt_context'].student_name,
        exercise_key=state['attempt_context'].exercise_key
    )

    print(f"\n== feature output ==\n{feature_output}\n")

    return {"feature_output": feature_output, "num_exercise_requirements": len(exercise_requirements)}


def student_profile_agent(state: GraphState):
    """Updates and tracks student proficiency of concepts by maintaining
    a exponential moving average of the scores of the concepts """

    print("\n== Student Profile Agent ==\n")

    # Get the past concepts scores
    past_concepts_scores = get_past_concept_scores(
        student_name=state['attempt_context'].student_name,
        exercise_key=state['attempt_context'].exercise_key,
        last_n=HISTORY_WINDOW
    )

    # print(f"\n== past concepts scores ==\n{past_concepts_scores}\n")

    # Get the concepts the students have implemented
    implemented_concepts: List[FeatureDetail] = state['feature_output'].implemented_concepts

    # Implemented concept scores
    implemented_concepts = {
        concept.tag: concept.score for concept in implemented_concepts
    }

    # print(f"\n== implemented concepts ==\n{implemented_concepts}\n")

    # Filter from the past concepts, the scores that are in implemented
    filtered_past_concepts = {
        key: past_concepts_scores[key] for key in implemented_concepts if key in past_concepts_scores
    }

    # print(f"\n== filtered past concepts ==\n{filtered_past_concepts}\n")

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

    if concept_emas:
        average_ema = sum(concept_emas.values()) / len(concept_emas)
    else:
        average_ema = 0.0

    no_progress_count = get_no_progress_count(
        student_name=state["attempt_context"].student_name,
        exercise_key=state["attempt_context"].exercise_key
    )

    # Decay average ema everytime the student is stuck
    if no_progress_count > 0:
        average_ema = average_ema * (STUCK_DECAY ** no_progress_count)

    # Update student profile with new scores
    update_student_profile(
        student_name=state['attempt_context'].student_name,
        exercise_key=state['attempt_context'].exercise_key,
        updated_scores=implemented_concepts,
        updated_emas=concept_emas,
        average_ema=average_ema
    )

    # Holds the ema and scores for the implemented concepts
    concept_ema_scores = {concept: {
        "score": implemented_concepts[concept], "ema": concept_emas[concept]} for concept in implemented_concepts}

    # print(f"\n== concept ema scores ==\n{concept_ema_scores}\n")

    return {"student_profile_output": StudentProfileOutput(implemented_ema_scores=concept_ema_scores, average_ema=average_ema)}


def issue_identifier_agent(state: GraphState):
    """Determines which concepts require attention"""
    print("\n== Issue Identifier Agent ==\n")

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

    # print(issue_identifier_output)

    return {"issue_identifier_output": issue_identifier_output}


def code_comparison_agent(state: GraphState):
    """Compares the student's previous and current code versions to 
    determine the quality of changes made"""
    print("\n== Code Comparison Agent ==\n")

    previous_code = get_previous_code(
        student_name=state['attempt_context'].student_name,
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
    # print(f"\n== code comparison output ==\n{code_comparison_output}\n")

    set_previous_code(
        student_name=state['attempt_context'].student_name,
        exercise_key=state['attempt_context'].exercise_key,
        previous_code=state['attempt_context'].student_code
    )

    # Update the no progress count if the logic is identical
    if code_comparison_output.identical_logic == "true":
        increment_no_progress_count(
            student_name=state['attempt_context'].student_name,
            exercise_key=state['attempt_context'].exercise_key
        )
    else:
        reset_no_progress_count(
            student_name=state['attempt_context'].student_name,
            exercise_key=state['attempt_context'].exercise_key
        )

    return {"code_comparison_output": code_comparison_output}


def hint_directive_agent(state: GraphState):
    """Decides the tonality and the type of hint to deliver"""
    print("\n== Hint Directive Agent ==\n")

    stuck_count = get_no_progress_count(
        student_name=state['attempt_context'].student_name,
        exercise_key=state['attempt_context'].exercise_key
    )

    print(f"\n== stuck count ==\n{stuck_count}\n")

    average_ema = state['student_profile_output'].average_ema
    feature_output = state['feature_output']
    issue_identifier_output = state['issue_identifier_output']

    print(f"average_ema : {average_ema}")

    # Natural language directives
    tone = "clear"
    strategy = ""
    rationale = ""

    # Set the tone based on whether the student is stuck or struggling
    if stuck_count > STUCK_ESCALATE and average_ema < STRUGGLE_EMA_THRESHOLD:
        tone = "beginner-friendly"
        rationale = "Student is stuck and struggling. The last hint didn't help. A short parallel example of possible syntax of some functionality will help. "
    elif stuck_count > STUCK_ESCALATE:
        tone = "beginner-friendly"
        rationale = "Student is stuck. The last hint didn't help. A conceptual hint will help. "
    elif average_ema > PROFICIENT_THRESHOLD and (len(feature_output.implemented_concepts) / state['num_exercise_requirements']) > HIGH_CONCEPT_COVERAGE:
        tone = "technical"
        rationale = "Student seems proficient. Perhaps a question to prompt deeper thinking. "

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

    error = state["attempt_context"].error
    test_results = state["attempt_context"].test_results

    # Fix Error Immediately if present
    if error:
        strategy = "Fix"
        rationale += f"Address the error at hand. Eg: 'seems like you have a syntax error'. Explain why the error exists, and a hint on how to fix it.\nError: {error}"
    else:
        if test_results:
            rationale += f"Acknowledge the student that tests have been ran. If tests fail, use it as context to provide a hint on why it is failing. \nTest Outcome: {test_results}"

        # Specify the issues
        if issue_identifier_output.issues:
            strategy = "conceptual" if average_ema < STRUGGLE_EMA_THRESHOLD else "reflective"
            rationale += "Issues Based on Importance:\n" + "\n".join(
                [f"{concept} - {detail}" for concept,
                    detail in list(issue_details.items())[:MAX_ISSUES]]
            )
        elif feature_output.missing_concepts:
            strategy = "next_step" if average_ema < STRUGGLE_EMA_THRESHOLD else "reflective"
            rationale += "Missing concepts:\n" + \
                ", ".join(feature_output.missing_concepts[:MAX_ISSUES])
        elif feature_output.redundant_concepts:
            strategy = "cleanup"
            rationale += f"Redundant concepts: {[f"{red.concept} - {red.detail}" for red in feature_output.redundant_concepts[:MAX_ISSUES]]}"
        else:
            print(
                f"\n== Fallback case where no issues / redundancies / missing_concepts detected ==\n")
            strategy = "reflective"
            rationale += "No issues detected. Encourage self-reflection, or optimisation techniques"

    print(
        f"\n== Hint Directive Output ==\nStrategy: {strategy}\nTone: {tone}\nRationale: {rationale}\n")

    return {
        "hint_directive": HintDirective(
            strategy=strategy,
            rationale=rationale,
            tone=tone
        )
    }


def hint_generator_agent(state: GraphState):
    """Responsible for generating the hint through an llm"""
    print("\n== Hint Generator Agent ==\n")

    previous_hint = get_previous_hint(
        student_name=state['attempt_context'].student_name,
        exercise_key=state['attempt_context'].exercise_key
    )
    print(f"\n== Previous hint ==\n{previous_hint}\n")

    prompt = hint_generator_prompt(
        exercise_text=state['attempt_context'].exercise_text,
        student_code=state['attempt_context'].student_code,
        hint_directive=state['hint_directive'],
        code_comparison_output=state['code_comparison_output'],
        previous_hint=previous_hint,
        improving_concepts=state['issue_identifier_output'].improving_concepts,
        struggling_concepts=state['issue_identifier_output'].struggling_concepts,
    )
    llm_input = [HumanMessage(content=prompt)]
    hint_output: HintOutput = llm.with_structured_output(
        HintOutput).invoke(llm_input)

    # print(f"\n== FINAL HINT ==\n{hint_output.hint_text}\n")

    set_previous_hint(
        student_name=state['attempt_context'].student_name,
        exercise_key=state['attempt_context'].exercise_key,
        previous_hint=hint_output.hint_text
    )

    return {"hint_output": hint_output}


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

        builder.add_node("hint_directive_agent", hint_directive_agent)

        builder.add_node("hint_generator_agent", hint_generator_agent)

        # == Add Edges ==
        builder.add_conditional_edges(
            START, decide_exercise_requirements_exists
        )

        builder.add_edge("exercise_requirement_agent",
                         "feature_extractor_agent")

        builder.add_edge("feature_extractor_agent", "student_profile_agent")

        builder.add_edge("student_profile_agent", "issue_identifier_agent")

        builder.add_edge("issue_identifier_agent", "code_comparison_agent")

        builder.add_edge("code_comparison_agent", "hint_directive_agent")

        builder.add_edge("hint_directive_agent", "hint_generator_agent")

        builder.add_edge("hint_generator_agent", END)

        self.graph = builder.compile()

    def run(self, state: GraphState):
        return self.graph.invoke(state)
