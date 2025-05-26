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
    exercise_key = "python_exercise3"

    exercise_title = "Reverse it"

    exercise_background = """Sometimes you want to undo a sequence of actions — like reversing steps in a to-do list. Let's write a function that flips a list.
    """

    exercise_text = "Write a function called `reverse_list` that takes a list and returns a new list with the elements in reverse order. Don't use any in-built methods. For Example:\n\n`reverse_list([1,2,3)] = [1,2,3]`\n\n`reverse_list([]) = []`"

    skel_code = """def reverse_list(numbers):
    return []

# Click Run to see what your function is doing. Try uncommenting below:
# print(reverse_list([1,2,3]))
    """

    test_cases = """
    import unittest, json

    class TestReverse(unittest.TestCase):
        def test_empty(self): self._run("emptyList", [], [])
        def test_single(self): self._run("singletonList", [5], [5])
        def test_pair(self): self._run("listOfNumbers", [4, 5], [5, 4])
        def test_multiple(self): self._run("listOfNumbers", [4, 5, 6, 6], [6, 6, 5, 4])
        
        def _run(self, name, input_val, expected):
            try:
                actual = reverse_list(input_val)
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

    # modify_exercise(exercise_key=exercise_key,
    #                 exercise_text=exercise_text)

    # delete_exercise("python_exercise2")

    get_or_create_exercise(
        exercise_key=exercise_key,
        exercise_background=exercise_background,
        exercise_text=exercise_text,
        skel_code=skel_code,
        exercise_title=exercise_title,
        test_cases=test_cases
    )

    # reset_student_exercise(student_name="ryan")

    print(f"\n== All Exercises: ==\n{list_all_exercises()}")
