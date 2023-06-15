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


template = """
            Task: Determine if anticoagulation is recommended based on the patient's CHA2DS2-VASc score, sex, and context.

            CHA2DS2-VASc Score: {score}

            Sex: {sex}

            Context: Most guidelines suggest that scores of 0 (men) or 1 (women) do not require treatment; however, all other patients should receive anticoagulation, preferably with a direct oral anticoagulant (unless contraindicated).
            Anticoagulation is not recommended in patients with non-valvular AF and a CHA2DS2-VASc score of 0 if male or 1 if female, as these patients had no TE events in the original study.
            Depending on a patient\'s preferences and individual risk factors, anticoagulation can be considered for a CHA2DS2-VASc score of 1 in males and 2 in females.
            Anticoagulation should be started in patients with a CHA2DS2-VASc score of >2 if male or >3 if female.

            Note: State if anticoagulation is recommended and nothing else. Only use the information from the context in your determination. Don't add any additional information. Limit your response to one sentence."""