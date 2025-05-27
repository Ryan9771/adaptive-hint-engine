exercise_key = "python_exercise5"

exercise_title = "Reverse it"

exercise_background = """At times, you may need to reverse a sequence of actions, to get the latest action first. Let's write a function that flips a list.
"""

exercise_text = "Modify the function `reverse_list` that takes a list and returns a **new list** with the elements in reverse order. Instead of using any in-built methods, you can use a simple loop to iterate through the list and construct the reversed list manually. Remember, you can use negative indexing to access elements from the end of the list. Example:\n\n`reverse_list([1,2,3]) = [3,2,1]`\n\n`reverse_list([]) = []`"

skel_code = """def reverse_list(numbers):
return []

# Click Run to check for syntax errors and to see what your function is doing. Try uncommenting below:
# print(reverse_list([1,2,3]))
"""

test_cases = """
import unittest, json

class TestLengths(unittest.TestCase):
    def test_empty(self): self._run("empty", [], [])
    def test_single(self): self._run("single", [5], [5])
    def test_pair(self): self._run("pair", [4, 5], [5, 4])
    def test_multiple(self): self._run("multiple", [4, 5, 6, 6], [6, 6, 5, 4])
    
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
