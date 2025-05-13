exercise_text = """
Given a list of integers, write a function that performs a convolution with a
kernel [1, 0, -1]. The convolution should be performed such that the output
list is the same length as the input list. To do this, we'll add a 0 to the start
and end of the list before performing the convolution.

Example:
Input: [1, 2, 3, 4, 5]
Kernel: [1, 0, -1]



Starting at index 1:
    Modified input: [0, 1, 2, 3, 4, 5, 0]
            Kernel: [1, 0, -1]

    0*1 + 1*0 + 2*-1 = -2

    convolved_values: [-2]

Now index 2:
    Modified input: [0, 1, 2, 3, 4, 5, 0]
            Kernel:    [1, 0, -1]

    1*1 + 2*0 + 3*-1 = -2

    convolved_values: [-2, -2]

We keep going until we reach the 2nd last element of the list (5).
"""

skel_code = """
def convolve(numbers: list[int]) -> list[int]:
    kernel = [1, 0, -1]
    numbers = [0] + numbers + [0]
    convolved_values = []

    return convolved_values
"""

# Note: Here is a code that passes all the tests but is not functionally correct
#   see string.length > 1

student_code = """
def convolve(numbers: list[int]) -> list[int]:
    kernel = [1, 0, -1]
    numbers = [0] + numbers + [0]
    convolved_values = []

    for i in numbers:
        convolved_values.append(numbers[i-1] * kernel[0] + numbers[i] * kernel[1] + numbers[i+1] * kernel[2])

    return convolved_values
"""

exercise_5 = {
    "exercise_key": "python_exercise5",
    "exercise_text": exercise_text,
    "skel_code": skel_code,
    "student_code": student_code,
    "language": "python"
}


# == RELATED HINT GENERATED (CCIS COMBINED)==
hint_1 = """
Consider each pixel in the image as a number either 0 or 1. To invert the image, you need to change each 0 to 1 and each 1 to 0. Think about how you can go through each element in the 2D list (which represents the image) and modify it. What programming construct can you use to iterate over the rows and columns of the image?
"""
