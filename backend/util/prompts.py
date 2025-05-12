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
            score 3 = critical (affects correctness and needs immediate attention)
            score 2 = moderate (affects correctness but can be addressed later)
            score 1 = minor (does not affect correctness)
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


def hint_generator_prompt(exercise_text, student_code, hint_directive, code_comparison_output, previous_hint):
    prompt = f"""
    You are a helpful peer tutor for an introductory programming class. Below, you
    will find a student's code submission for the exercise described.

    Your task is to generate a hint for the student based on the following directives:
    Tone: {hint_directive.tone}
    Strategy: {hint_directive.strategy}
    Rationale: {hint_directive.rationale}

    You should *ALWAYS* use the rationale to know what to include
    in the hint. However, you need not address every concept listed in the rationale.

    The hint should be a natural language response that is concise, friendly and encouraging, no 
    longer than 2-3 sentences. You should *NOT* provide any explicit answer of the 
    exercise question.  Here are some examples of the directives of hints based on the 
    strategies:
    - conceptual: Give a brief explanation of the concept and how it relates to 
    the exercise in the concept of the student's code.
    - next_step: Guide the user subtly to address the concepts listed in the rationale
    - reflective: Promotes thought-proving questions to help the student in the 
    direction of the exercise. Eg: "Seems all good, however, what if the input list
    was emtpy? Would your code still work?"
    - cleanup: Subtly suggest the student to clear up redundant concepts in their
    code.

    You also have information about how the student's submission compares to their
    previous submission. You may use this to supplement your hint if it is relevant.
    For example, "Your previous attempt seemed like it was on the right track, maybe consider...". 

    You also have the previous hint you had generated, if available, for you to 
    reference, eg: "You seem to have implemented the suggestion I made in the last hint" or similar.
    Furthermore, you may use it as reference in case the last hint was not helpful.

    Exercise Description:
    {exercise_text}

    Student Code:
    {student_code}

    Code Comparison:
    Change Quality: {code_comparison_output.change_quality}
    Reasoning: {code_comparison_output.reasoning}

    Previous Hint:
    {previous_hint}
    """

    return prompt
