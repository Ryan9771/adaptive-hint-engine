exercise_key = "python_exercise6"

exercise_title = "Count the words"

exercise_background = """A simple word counter could be good to check whether a text is too long or short."""

exercise_text = "Modify the function `count_words` that takes a string (a sentence) and returns how many words there are. Words are separated by spaces. Do not use any in-built functions. For example:\n\n`count_words('hello world') = 2`\n\n`count_words('Planes fly very high') = 4`"

skel_code = """def count_words(sentence):
return 0

# Click Run to check for syntax errors and to see what your function is doing. Try uncommenting below:
# print(count_words("hello"))
"""

test_cases = """
import unittest, json

class TestLengths(unittest.TestCase):
    def test_two_words(self): self._run("two_words", "hello world", 2)
    def test_four_words(self): self._run("four_words", "Planes fly very high", 4)
    def test_one_word(self): self._run("one_word", "hello", 1)
    def test_empty_string(self): self._run("empty_string", "", 0)
    
    def _run(self, name, input_val, expected):
        try:
            actual = count_words(input_val)
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
