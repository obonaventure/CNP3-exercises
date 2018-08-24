import subprocess
from inginious import feedback, input

def get_single_line_answer(problem_id):
    """Return the answer of the student to the question identified by the argument.
    Return "NONE" if the answer was "None", otherwise return a list of string which
    is the answer of the student, split by the coma."""

    answer = input.get_input(problem_id).upper()
    if answer == "NONE":
        return answer
    answer = ''.join(answer.split()) # remove spaces
    return answer.split(",")

def get_multiple_line_answer(problem_id):
    """Return the answer of the student to the question identified by the argument.
    Return "NONE" if the answer was "None", otherwise return a bidimensional list,
    where the the first list is a split of the answer according to new lines, and
    the second list according to comas. (Example: "1,2,3\n4,4,6" will return 
    [[1, 2, 3], [4, 5, 6]])"""

    answer = input.get_input(problem_id).upper()
    if answer == "NONE":
        return answer
    answer = ''.join(answer.split()) # remove spaces
    return [a.split(",") for a in answer.split("\n")]

def set_problem_result(problem_id, result, fb):
    """Set the result and the feedback to a problem."""

    feedback.set_problem_result(result, problem)
    feedback.set_problem_feedback(fb, problem)

def shuffle(list_to_shuffle):
    """Shuffle a list. This method is used instead of the method provided in python
    so that it matches the shuffle method used in javascript.""""

    n = len(list_to_shuffle)
    while n > 0:
        index = get_random(n-1, n)
        n = n-1
        temp = list_to_shuffle[n]
        list_to_shuffle[n] = list_to_shuffle[index]
        list_to_shuffle[index] = temp

def get_random(i=0, upper=1000):
    """Return a random number.

    :optional param i: The index of the random number of INGInious.
    :optional param upper: The upper bound of the random number. The default is 1000
    """
    
    return int(input.get_input("@random")[i]*upper)