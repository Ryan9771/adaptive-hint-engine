exercise_text = """
Return a list of numbers without any duplicates!

Eg:

remove_duplicates([1, 1, 1, 2, 2, 2]) should equal [1, 2]
"""

skel_code = """
def remove_duplicates(numbers: list[int]) -> list[int]:
    list_without_duplicates = []

    return list_without_duplicates
"""

# Note: Here is a code that passes all the tests but is not functionally correct
#   see string.length > 1

student_code = """
def remove_duplicates(numbers: list[int]) -> list[int]:
    list_without_duplicates = []

    for number in numbers:
        if number not in list_without_duplicates:
            list_without_duplicates.append(number)

    


    return list_without_duplicates
"""

exercise_2 = {
    "exercise_key": "python_exercise2",
    "exercise_text": exercise_text,
    "skel_code": skel_code,
    "student_code": student_code,
    "language": "python"
}


# == RELATED HINT GENERATED (CCIS COMBINED)==
hint_1 = """
Think about how you can keep track of numbers you've already seen as you go through the list. Consider using a data structure that automatically handles duplicates for you. Can you think of a way to iterate over the numbers and add them to this data structure, then use it to build your final list?
"""

hint_1_modified = """
Think about how you can keep track of numbers you've already seen as you go through the list. Consider using a data structure. Can you think of a way to iterate over the numbers and add them to this data structure?
"""

hint_2 = """
Think about how you can go through each number in the list and check if it's already in your `list_without_duplicates` before adding it. What Python structure allows you to repeat actions for each item in a list? How can you use a conditional statement to decide whether or not to add a number to your list? Try implementing these steps to build up your function.
"""
