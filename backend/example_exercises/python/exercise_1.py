exercise_key = "python_exercise1"

exercise_title = "Is it Even?"

exercise_background = """Imagine you're building a game where players take turns based on whether their score is even or odd. You need a quick way to check that!
"""

exercise_text = "Modify the function `is_even` that takes an integer and returns `True` if it's even and `False` if it's odd. Do not use any in-built functions. For Example:\n\n`is_even(4) = True`\n\n`is_even(0) = True`"

skel_code = """def is_even(n):
return False

# Click Run to check for syntax errors and to see what your function is doing. Try uncommenting below:
# print(is_even(4))
"""

test_cases = """
import unittest, json

class TestLengths(unittest.TestCase):
    def test_zero(self): self._run("zero", 0, True)
    def test_five(self): self._run("five", 5, False)
    def test_seven(self): self._run("seven", 7, False)
    def test_hundred_two(self): self._run("hundred_two", 102, True)
    
    def _run(self, name, input_val, expected):
        try:
            actual = is_even(input_val)
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
