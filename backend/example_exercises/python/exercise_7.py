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
