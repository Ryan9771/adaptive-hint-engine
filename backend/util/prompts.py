def exercise_requirements_prompt(exercise_text, skel_code):
    prompt = f"""
    You are an expert programming tutor. Given a programming exercise and its 
    skeleton code, list the key programming concepts that a correct solution 
    must demonstrate.

    Focus only on concepts that are essential to solving the problem 
    (e.g., loops, conditionals, recursion, list indexing, string formatting). 
    Do not include concepts that are optional or stylistic.

    Exercise Description:
    {exercise_text}

    Skeleton Code:
    {skel_code}
    """


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
