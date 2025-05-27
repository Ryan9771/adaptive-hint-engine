exercise_key = "python_exercise4"

exercise_title = "Count the Vowels"

exercise_background = """At times, you might have wanted to count the number of vowels in a string. This is a common task in text processing and can be useful for various applications, such as analyzing text data or creating simple games.
"""

exercise_text = "Modify the function `count_vowels` that takes a string and returns the number of vowels in it. Use a simple loop structure to iterate through the string and count the vowels. For Example:\n\n`count_vowels('hello') = 2`\n\n`count_vowels('sky') = 0`\n\n`count_vowels('aeiou') = 5`"

skel_code = """def count_vowels(word):
return 0

# Click Run to check for syntax errors and to see what your function is doing. Try uncommenting below:
# print(count_vowels("hello"))
"""

test_cases = """
import unittest, json

class TestLengths(unittest.TestCase):
    def test_no_vowels(self): self._run("no_vowels", "sky", 0)
    def test_a_vowel(self): self._run("a_vowel", "ban", 1)
    def test_two_vowels(self): self._run("two_vowels", "meet", 2)
    def test_many_vowels(self): self._run("all_vowels", "haeiou", 5)
    
    def _run(self, name, input_val, expected):
        try:
            actual = count_vowels(input_val)
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
