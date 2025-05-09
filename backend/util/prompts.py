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
        a. Aassign a score between 1 and 4 based on your judgment on the 
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
