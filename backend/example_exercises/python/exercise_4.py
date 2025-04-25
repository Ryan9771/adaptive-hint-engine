exercise_text = """
Given a black and white image, where each pixel is either black (0) or white (1),
invert an image such that all black pixels are white and vice versa.

Eg:

image_1 = [
    [1, 0, 0, 1, 1, 1],
    [0, 1, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 1],
    [0, 1, 0, 0, 1, 1],
    [1, 0, 0, 1, 1, 1],
]

invert_image(image_1) = [
    [0, 1, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 0],
    [0, 1, 1, 0, 1, 0],
    [1, 0, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 0],
]
"""

skel_code = """
def invert_image(image):

    return image
"""

# Note: Here is a code that passes all the tests but is not functionally correct
#   see string.length > 1

student_code = """
def invert_image(image):

    return image
"""

exercise_4 = {
    "exercise_key": "python_exercise_4",
    "exercise_text": exercise_text,
    "skel_code": skel_code,
    "student_code": student_code,
    "language": "python"
}


# == RELATED HINT GENERATED (CCIS COMBINED)==
hint_1 = """
Consider each pixel in the image as a number either 0 or 1. To invert the image, you need to change each 0 to 1 and each 1 to 0. Think about how you can go through each element in the 2D list (which represents the image) and modify it. What programming construct can you use to iterate over the rows and columns of the image?
"""
