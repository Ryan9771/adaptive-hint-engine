from setup_db import engine, Base, add_exercise, list_all_exercises, delete_exercise

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
    exercise_key = "python_exercise3"

    exercise_title = "Palindromes"

    exercise_background = """A palindrome is something that reads the same 
    forward and backward. You may have seen palindromes in words like "level" or 
    "racecar", but numbers and lists can be palindromes too. For example, the 
    list [1, 2, 3, 2, 1] is a palindrome because it is the same when read from 
    left to right and from right to left.
    """

    exercise_text = """Write a program that checks if a list of numbers is a 
    palindrome. The program should return true if the list is the same forwards 
    and backwards, and false otherwise. You should not use any built-in 
    functions that reverse the list. Use loops and if statements to compare the 
    elements from both ends of the list. 
    """

    skel_code = """
    def is_palindrome(numbers: list[int]) -> bool:

        return False
    """

    # delete_exercise(exercise_key)

    add_exercise(
        exercise_key=exercise_key,
        exercise_background=exercise_background,
        exercise_text=exercise_text,
        skel_code=skel_code,
        exercise_title=exercise_title
    )

    print(f"\n== All Exercises: ==\n{list_all_exercises()}")
