exercise_text = """
A list is a palindrome if it is exactly the same when reversed. For example:
[1] is a palindrome, [1, 2, 2, 1] is also a palindrome. But [1, 2] and 
[1, 5, 2, 1] are not.

Given a list of numbers, return True if the list is a palindrome and False 
if it isn't.

You are not allowed to use built in reverse methods!

For example 
    is_palindrome([1, 2, 3, 2, 1]) = True
    is_palindrome([1, 2, 3, 1, 3]) = False
"""

skel_code = """
def is_palindrome(numbers: list[int]) -> bool:

    return False
"""

# Note: Here is a code that passes all the tests but is not functionally correct
#   see string.length > 1

student_code = """
def is_palindrome(numbers: list[int]) -> bool:

    is_palindrome = True

    for i in range(len(numbers)):
        if i != numbers[len(numbers) - i]:
            is_palindrome = False


    return is_palindrome
"""

exercise_3 = {
    "exercise_key": "python_exercise3",
    "exercise_text": exercise_text,
    "skel_code": skel_code,
    "student_code": student_code,
    "language": "python"
}


# == RELATED HINT GENERATED (CCIS COMBINED)==
hint_1 = """
Think of a palindrome as a sequence that reads the same forwards and backwards. To check if the list is a palindrome, try comparing the elements starting from the beginning of the list with those from the end, moving towards the center. Can you think of a way to achieve this using a loop? You could try comparing elements at indices `i` and `-(i+1)` for a range of `i` values.
"""

# == Progress 1 ==
"""
def is_palindrome(numbers: list[int]) -> bool:

    is_palindrome = True

    for i in range(len(numbers)):
        if i != numbers[len(numbers) - i]:
            is_palindrome = False


    return is_palindrome
"""

# Hint
"""
To check if a list is a palindrome, focus on comparing the elements from the start and the end of the list moving towards the center. Currently, your loop's comparison logic is a bit off. Here's a hint to guide you:

Instead of comparing `i` with `numbers[len(numbers) - i]`, think about comparing `numbers[i]` with `numbers[len(numbers) - 1 - i]`. This adjustment will help you correctly check if the elements from both ends are equal. Additionally, remember to stop your loop at the halfway point of the list to avoid unnecessary comparisons. Try adjusting your loop logic to focus on these comparisons, and see how this affects your program.
"""
