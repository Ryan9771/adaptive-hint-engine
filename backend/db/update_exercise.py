from setup_db import engine, Base, add_exercise, list_all_exercises, delete_exercise, modify_exercise

"""
Exercise Detail Format:

exercise_title - Title
exercise_background - Text before instructions
exercise_text - Exercise Instructions
skel_code - Default code

"""


if __name__ == "__main__":
    # Create the database
    Base.metadata.create_all(bind=engine)

    # Create the exercises
    exercise_key = "python_exercise1"

    exercise_title = "Is it Even?"

    exercise_background = """Imagine you're building a game where players take turns based on whether their score is even or odd. You need a quick way to check that!
    """

    exercise_text = """Write a function called is_even that takes an integer and returns True if it’s even and False if it’s odd.

    For Example:
    `isEven(4) = True`
    `isEven(0) = True`
    `isEven(3) = False`
    """

    skel_code = """def isEven(n):
    pass
    """

    # modify_exercise(exercise_key=exercise_key,
    #                 exercise_text=exercise_text)

    # delete_exercise("python_exercise2")

    add_exercise(
        exercise_key=exercise_key,
        exercise_background=exercise_background,
        exercise_text=exercise_text,
        skel_code=skel_code,
        exercise_title=exercise_title
    )

    print(f"\n== All Exercises: ==\n{list_all_exercises()}")
