question = """
Write a function lengths() that takes a list of strings and returns a list of their lengths:
"""

skel_code = """
fun lengths() = TODO()
"""

# Note: Here is a code that passes all the tests but is not functionally correct
#   see string.length > 1

student_code = """
fun lengths(strings: List<String>): List<Int> {
    val res = mutableListOf<Int>()
    for (string in strings) {
        if (string.length > 1) {
            res.add(string.length) 
        } 
    }

    return res
}
"""

exercise_1 = {
    "question": question,
    "skel_code": skel_code,
    "student_code": student_code,
}
