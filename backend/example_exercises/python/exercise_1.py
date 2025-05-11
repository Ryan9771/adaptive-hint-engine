exercise_text = """
Description: Print numbers from 1 to n. For multiples of 3, print "Fizz", for multiples of 5, print "Buzz", and for multiples of both, print "FizzBuzz".
"""

skel_code = """
def fizzbuzz(n):
    pass
"""

# Note: Here is a code that passes all the tests but is not functionally correct
#   see string.length > 1

student_code = """
def fizzbuzz(n):
    for i in range(1, n+1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
"""

# student_code = """
# def fizzbuzz(n):
#     for i in range(1, n+1):
#         if i % 3 == 0:
#             print("Fizz")
#         else:
#             print("Buzz")

#         print("FizzBuzz)
# }
# """

exercise_1 = {
    "exercise_key": "python_exercise_1",
    "exercise_text": exercise_text,
    "skel_code": skel_code,
    "student_code": student_code,
    "language": "python"
}
