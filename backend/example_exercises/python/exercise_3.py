exercise_key = "python_exercise3"

exercise_title = "Find the maximum"

exercise_background = """You're writing a program to find the highest score in a game. How do you figure out which number is the biggest in a list?
"""

exercise_text = "Write a function called `find_max` that takes a list of numbers and returns the largest one. Assume the list has at least one number. Do not use any in-built functions. For example:\n\n`find_max([5, 2, 3]) = 5`\n\n`find_max([-5, -10, -2]) = -2`"

skel_code = """def find_max(numbers):
return 0

# Click Run to check for syntax errors and to see what your function is doing. Try uncommenting below:
# print(find_max([1, 2, 3]))
"""

test_cases = """
import unittest, json

class TestLengths(unittest.TestCase):
    def test_single(self): self._run("single", [5], 5)
    def test_pair(self): self._run("pair", [4, 5], 5)
    def test_multiple(self): self._run("multiple", [4, 5, 6, 6], 6)
    def test_negative(self): self._run("negative", [-5, -10, -2], -2)
    
    def _run(self, name, input_val, expected):
        try:
            actual = find_max(input_val)
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
