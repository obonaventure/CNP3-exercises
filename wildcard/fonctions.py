import gettext

def init_translations():
    """
        Move the translations files to student directory
        Initialize gettext and translate to the proper language
    """
    lang = input.get_lang()
    try:
        trad = gettext.GNUTranslations(open("../course/common/student/$i18n/" + lang + ".mo", "rb"))
    except FileNotFoundError:
        trad = gettext.NullTranslations()
    trad.install()
    return lang

def correct_qcm(question_id, responses):
    """
       Question_id est l'id de la question et responses sont toutes les questions possibles du QRM. 
       Corrige un qcm à réponses multiples.
    """
    ticked = input.get_input(question_id)
    if len(ticked) != len(responses):
        feedback.set_problem_result("failed", "flags")
        feedback.set_problem_feedback(_("You don't have the right number of answer"), "flags")
        return False
    for i in responses:
        if i not in ticked:
            feedback.set_problem_result("failed", "flags")
            feedback.set_problem_feedback(_("This is not the good answer"), "flags")
            return False
    return True

def is_elem_in_order(problem_id, list_name, elem):
    last = -1
    for i in elem:
        actual = int(input.get_input("{}-{}-pos".format(problem_id, i)).split('#')[-1])
        if actual < last:
            return False
        last = actual
    return True

def test_perm_croisee(problem_id, list_name, list_of_lists):
    """return True if all the groups are individually well sorted.
       In list_of_lists you have to enter all the lists that compose a group.
       Each group must be sorted like the student has to sort it."""
    for elem in list_of_lists:
        if not is_elem_in_order(problem_id, list_name, elem):
            return False
    return True

def test_my_list(problem_id, list_name, number_of_elements):
    """return the number of error(s) of the student!
       The id's are from 0 to number_of_elements not included."""
    errors = 0
    for i in range(number_of_elements):
        if input.get_input("{}-{}-pos".format(problem_id, i)) != "{}#{}".format(list_name, i):
            errors += 1
    return errors