def chads_vasc_score(age: int, female: bool, chf: bool, hypertension: bool, stroke_tia: bool, vascular_disease: bool, diabetes: bool) -> int:
    """
    Calculate the CHA2DS2-VASc score based on input parameters.

    :param age: integer, patient's age
    :param female: bool, if patient is female
    :param chf: boolean, presence of congestive heart failure
    :param hypertension: boolean, presence of hypertension
    :param stroke_tia: boolean, history of stroke or transient ischemic attack
    :param vascular_disease: boolean, presence of vascular disease
    :param diabetes: boolean, presence of diabetes
    :return: integer, CHA2DS2-VASc score
    """
    score = 0

    # Age
    if age >= 65 and age < 75:
        score += 1
    elif age >= 75:
        score += 2

    # Female
    if female:
        score += 1

    # CHF
    if chf:
        score += 1

    # Hypertension
    if hypertension:
        score += 1

    # Stroke or TIA
    if stroke_tia:
        score += 2

    # Vascular Disease
    if vascular_disease:
        score += 1

    # Diabetes
    if diabetes:
        score += 1

    return score
