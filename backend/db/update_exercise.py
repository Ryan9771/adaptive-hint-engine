from setup_db import engine, Base, get_or_create_exercise, list_all_exercises, delete_exercise, modify_exercise, reset_student_exercise

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
    exercise_key = "python_exercise7"

    exercise_title = "Palindromes"

    exercise_background = """Palindromes are words or phrases that read the same backward as forward. They can be fun to identify and work with in programming."""

    exercise_text = "Modify the function `check_palindrome` that takes a string and returns `True` or `False` based on whether its a palindrome. Do not use any in-built functions. For example:\n\n`check_palindrome('racecar') = True`\n\n`check_palindrome('hello') = False`"

    skel_code = """def check_palindrome(word):
    return False 

# Click Run to check for syntax errors and to see what your function is doing. Try uncommenting below:
# print(check_palindrome("hello"))
    """

    test_cases = """
import unittest, json

class TestLengths(unittest.TestCase):
    def test_palindrome(self): self._run("palindrome", "racecar", True)
    def test_not_palindrome(self): self._run("not_palindrome", "hello", False)
    def test_empty_string(self): self._run("empty_string", "", True)
    def test_single_character(self): self._run("single_character", "a", True)
    
    def _run(self, name, input_val, expected):
        try:
            actual = check_palindrome(input_val)
            print("@@TEST_RESULT@@", json.dumps({
                "input": input_val,
                "expected": expected,
                "actual": actual,
                "passed": actual == expected
            }))
        except Exception as e:
            print("@@TEST_RESULT@@", json.dumps({
                "input": input_val,
                "expected": expected,
                "actual": str(e),
                "passed": False
            }))

if __name__ == "__main__":
    unittest.main()
    """


modify_exercise(
    exercise_key=exercise_key,
    exercise_text=exercise_text,
    # skel_code=skel_code
)

# delete_exercise("python_exercise2")

# get_or_create_exercise(
#     exercise_key=exercise_key,
#     exercise_background=exercise_background,
#     exercise_text=exercise_text,
#     skel_code=skel_code,
#     exercise_title=exercise_title,
#     test_cases=test_cases
# )

# reset_student_exercise(student_name="ryan")

print(f"\n== All Exercises: ==\n{list_all_exercises()}")
