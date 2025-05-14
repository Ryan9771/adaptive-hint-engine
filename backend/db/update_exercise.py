from setup_db import engine, Base, add_exercise, list_all_exercises

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

    # Exercise 2 == Remove Duplicates
    exercise_key = "python_exercise2"

    exercise_title = "Removing Duplicates from a List"

    exercise_background = """Sometimes a list contains repeated values, but you 
    only want to keep one copy of each. For example, if a list has the numbers 
    1, 2, 2, 3, and 1, you may want to create a new list that just has 1, 2, 
    and 3 in the order they first appeared. This exercise is about going through 
    a list and collecting only the first occurrence of each number."""

    exercise_text = """Write a program that takes a list of numbers and returns 
    a new list with all duplicates removed. You should not use any built-in 
    functions or data structures that automatically remove duplicates, such as 
    sets. 
    """

    skel_code = """
        def remove_duplicates(numbers: list[int]) -> list[int]:
            pass
    """

    add_exercise(
        exercise_key=exercise_key,
        exercise_background=exercise_background,
        exercise_text=exercise_text,
        skel_code=skel_code,
        exercise_title=exercise_title
    )

    print(f"\n== All Exercises: ==\n{list_all_exercises()}")
