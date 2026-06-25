def route_question(question: str):

    q = question.lower()

    if "postal" in q or "postcode" in q:
        return "postal"

    if "district" in q:
        return "district"

    return "district"   # safe default