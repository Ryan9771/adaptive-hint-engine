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
        "modulo_operator",
        "conditional_statements",
        "comparison_operations",
        "print_statements",
        "integer_literals",
        "boolean_logic",
        "range_function",
        "nested_conditionals",
        "string_output_construction"
    ]

    Exercise Description:
    {exercise_text}

    Skeleton Code:
    {skel_code}
    """

    return prompt


def feature_extractor_prompt(exercise_text, skel_code, student_code):
    prompt = f"""
    Analyse this student submission for key programming concepts:
    Exercise Description: {exercise_text}
    Skeleton:
    {skel_code}
    Submission:
    {student_code}
    """
    pass
