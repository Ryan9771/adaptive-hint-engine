def exercise_requirements_prompt(exercise_text, skel_code):
    prompt = f"""
    You are an expert programming teacher tasked to provide a list of concepts 
    from an exercise that an llm would need to use to compare with a student's 
    implementation. List the core programming concepts that are **functionally**
    necessary to solve the exercise below. (Eg: boolean conditions, loops etc..)

    Do not include concepts that are optional or stylistic. You should not 
    provide any explanations or codes. Multi-word concepts should be joined by
    underscores. 

    For example, for a FizzBuzz problem, the output should look something like:
    [
        "loops",
        "range_function",
        "modulo_operator",
        "conditional_statements",
        "comparison_operations",
        "print_statements",
        "integer_literals",
        "boolean_logic",
        "nested_conditionals",
        "string_output_construction"
    ]

    Exercise Description:
    {exercise_text}

    Skeleton Code:
    {skel_code}
    """

    return prompt


def feature_extractor_prompt(exercise_requirements, exercise_text, skel_code, student_code):
    prompt = f"""
    You are an expert code reviewer for beginner programming students. 
    Your task is to analyze a student's code submission for a given exercise.

    Instructions:

    1. For each core functional concept used in the student's code:
        a. Assign a score between 1 and 4 based on your judgement on the 
        excercise goals and constraints:
            - 4 = used correctly and appropriately
            - 3 = mostly correct, but with minor mistakes (e.g. loop has bounds off by one)
            - 2 = attempted but significantly incorrect
            - 1 = present but fundamentally wrong or misused
        b. If the score is less than 4, briefly describe the issue (max one sentence)
        c. Try to match the concept to one of the following canonical exercise
        requirement tags. If the concept doesn't match, invent a new tag using
        snake_case: 
        Exercise Requirements: {exercise_requirements}
    
    2. List any missing concepts from the exercise requirements. If additional 
    concepts are needed, include them in snake_case format.

    3. List any redundant concepts used in the student code that are not required. 
        a. For each redundant concept, assign a severity score between 1
        and 3 where:
            3 = critical (affects correctness and needs immediate attention)
            2 = moderate (affects correctness but can be addressed later)
            1 = minor (does not affect correctness)
        b. Briefly explain why it is redundant (max one sentence).

    Exercise Description:
    {exercise_text}
    
    Skeleton Code:
    {skel_code}

    Student Code:
    {student_code}
    """

    return prompt


def code_comparison_prompt(exercise_text, previous_code, current_code):
    prompt = f"""
    You are an expert programming tutor. Your job is to compare a student's 
    *previous* and *current* code submissions for the same exercise based on
    the following criteria:

    1. Identical logic - true / false
        true - the 2 snippets are functionally identical (any differences are only 
        whitespace, comments or trivial renamings)
        false - logic or control-flow changed

    2. Change Quality - improving / regressing / same
        Decide which snippet is closer to a correct, idiomatic solution to the 
        exercise. 
    
    3. Reasoning - If the change quality is improving or regressing, provide one 
    sentence explaining why, and a one sentence high level overview of what 
    you think the student is trying to do and how well they are doing it based
    on the exercise description.

    Exercise Description:
    {exercise_text}

    Previous Submission:
    {previous_code}

    Current Submission:
    {current_code}
    """

    return prompt


def hint_generator_prompt(exercise_text, student_code, hint_directive, code_comparison_output, previous_hint, improving_concepts, struggling_concepts):
    prompt = f"""
    You are a friendly peer tutor for beginner programming students.

    ## **HARD RULES**
    - ≤ 3 sentences, Markdown.
    - Encourage; never illustrate sequence of steps to directly solve the exercise. Provide incremental help.
    - *Example* permitted below hint **only if** the rationale requests it:
        • show ≤ 1 small syntax fragment in a different setting. Eg: how to use a for loop  
        • fragment should demonstrate a single sub-concept in a beginner-friendly way
        • make it non-copyable (change names, inputs, context)

    ## **STRATEGY BEHAVIOUR**  
    | Strategy      | Required hint features (include **only** for this strategy)                    |
    | ------------- | ----------------------------------------------------------------------------- |
    | conceptual    | Briefly clarify the key concept and why it matters here.                      |
    | next_step     | Nudge towards the next logical concept in the rationale                              |
    | reflective    | Aid students with thought provoking questions (e.g. “Good job, but what if the list is empty?”) |
    | cleanup       | Suggest redundant / dead code to trim or refactor.                            |
    | fix           | Address the rationale        |

    ## **TONE, STRATEGY, RATIONALE**
    Tone: {hint_directive.tone} - (Note: Unless 'technical', a 'clear' tone should be easy to understand by novice programmers, and 'beginner-friendly' should be even simpler to understand)
    Strategy: {hint_directive.strategy}
    Rationale (Use as guidance; you need not address every concept listed): 
    {hint_directive.rationale}

    ## **CONTEXT SNAPSHOT**
    - Previous vs Current Code Submission Change Quality: {code_comparison_output.change_quality} - {code_comparison_output.reasoning}
    - Previous hint you generated: {previous_hint}
    - Improving Concepts: {improving_concepts}
    - Struggling Concepts: {struggling_concepts}

    !! Adapt: Acknowledge progress or setbacks. Eg: "Seems like you've implemented the last hint well, however.." / 
    "you are getting better at loops" / "you seem to have not changed anything". You may also adapt your hint based on your
    previous hint.

    ---- 
    Exercise Description:
    {exercise_text}

    Student Code:
    ```python
    {student_code}
    ```
    """

    return prompt
