exercise_key = "python_exercise2"

exercise_title = "Absolute Difference"

exercise_background = """The absolute difference between two numbers is a simple way to find out how far apart they are."""

exercise_text = "Modify the function `absolute_difference` that takes two integers and returns the absolute difference between them. Do not use any in-built functions. For example:\n\n`absolute_difference(5, 3) = 2`\n\n`absolute_difference(3, 5) = 2`\n\n`absolute_difference(-1, -4) = 3`"

skel_code = """def absolute_difference(a, b):
return 0

# Click Run to check for syntax errors and to see what your function is doing. Try uncommenting below:
# print(absolute_difference(1, 2))
"""

test_cases = """
import unittest, json

class TestLengths(unittest.TestCase):
    def test_positive_difference(self): self._run("positive_difference", 5, 3, 2)
    def test_reverse_difference(self): self._run("reverse_difference", 3, 5, 2)
    def test_negative_difference(self): self._run("negative_difference", -5, -2, 3)
    def test_zero_difference(self): self._run("zero_difference", 4, 4, 0)
    
    def _run(self, name, input_val_a, input_val_b, expected):
        try:
            actual = absolute_difference(input_val_a, input_val_b)
            print("@@TEST_RESULT@@", json.dumps({
                "input": (input_val_a, input_val_b),
                "expected": expected,
                "actual": actual,
                "passed": actual == expected
            }))
        except Exception as e:
            print("@@TEST_RESULT@@", json.dumps({
                "input": (input_val_a, input_val_b),
                "expected": expected,
                "actual": str(e),
                "passed": False
            }))

if __name__ == "__main__":
    unittest.main()
"""
