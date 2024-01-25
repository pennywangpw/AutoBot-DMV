from random import choice, randint

def check_keyword(user_input: str) -> str:
    date_keyword = ["date", "earlier", "dates"]
    distance_keyword = ["miles", "mile"]
    print("user_input and type", user_input, type(user_input))
    split_user_input = user_input.split()

    for word in split_user_input:
        print("word: ",word)
        if word in date_keyword:
            return f"Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"

        elif word in distance_keyword:
            return f"Hey ~ Please provide the date(YYYY-MM-DD) zipcode (i.e. 98087) specific mile(i.e. 7 miles)"

    return False


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    response_by_keyword_check = check_keyword(lowered)

    if not response_by_keyword_check:
        return choice(['I do not understand...','Do you mind rephrasing that?'])

    else:
        return response_by_keyword_check
