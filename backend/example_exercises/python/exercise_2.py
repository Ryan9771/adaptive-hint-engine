exercise_key = "python_exercise2"

exercise_title = "FizzBuzz"

exercise_background = """FizzBuzz is a classic challenge often asked in coding interviews and quizzes. It's a fun way to test how well you handle multiple conditions!"""

exercise_text = """Write a function called fizz_buzz that takes an integer:
- Returns "FizzBuzz" if divisible by 3 and 5,
- Returns "Fizz" if divisible by 3,
- Returns "Buzz" if divisible by 5,
- Otherwise, return the number as a string.

For example:
`fizz_buzz(15) = "FizzBuzz"`
`fizz_buzz(9) = "Fizz"`
`fizz_buzz(10) = "Buzz"`
`fizz_buzz(7) = "7"`
"""

skel_code = """def fizz_buzz(n):
pass
"""

test_ex_2 = """
import unittest, json

class TestLengths(unittest.TestCase):
    def test_empty(self): self._run("emptyList", [], [])
    def test_single(self): self._run("singletonList", [5], [5])
    def test_pair(self): self._run("listOfNumbers", [4, 4], [4])
    def test_multiple(self): self._run("listOfNumbers", [4, 5, 6, 6], [4, 5, 6])
    
    def _run(self, name, input_val, expected):
        try:
            actual = remove_duplicates(input_val)
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
