from random import choice, randint
from Validation_Handler import ValidationHandler


validation_handler= ValidationHandler()


def check_keyword(user_input: str) -> str:
    date_keyword = ["date", "earlier", "dates"]
    distance_keyword = ["miles", "mile"]
    print("user_input and type", user_input, type(user_input))

    #check user input includes 2 data -> 1.date 3. zipcode
    if_in_keyword = False
    if_date_and_zipcode = False
    split_user_input_list = user_input.split()
    user_input_validation = validation_handler.date_zipcode_input_validation_V2(split_user_input_list)
    print("user_input_validation: ",user_input_validation)


    if user_input_validation == "pass":
        if_date_and_zipcode = True

    # find if there's any keyword in user input
    else:
        for word in split_user_input_list:
            print("word: ",word)
            if word == "hello" or word =="hi":
                if_in_keyword = True
                return "Hello there! How can I help you ?"
            elif word in date_keyword:
                if_in_keyword = True
                return f"Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"

            elif word in distance_keyword:
                if_in_keyword = True
                return f"Hey ~ Please provide the date(YYYY-MM-DD) zipcode (i.e. 98087) specific mile(i.e. 7 miles)"

            #     if_in_keyword = True
            #     return f"Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"

            # elif word in distance_keyword:
            #     if_in_keyword = True
            #     return f"Hey ~ Please provide the date(YYYY-MM-DD) zipcode (i.e. 98087) specific mile(i.e. 7 miles)"

            # elif word == "hello":
            #     if_in_keyword = True
            #     return "Hello there! How can I help you ?"

            # elif validation_handler.check_datetime_formate_validation(word):
            #     if_in_keyword = True
            #     return f"your input {word} is valid date time"

            # elif validation_handler.check_convert_into_num(word) and validation_handler.check_length_zipcode_input_validtion(word):
            #     if_in_keyword = True
            #     return f"your input {word} is valid zipcode"



    if not if_in_keyword or not if_date_and_zipcode:
        return False


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    response_by_keyword_check = check_keyword(lowered)

    if not response_by_keyword_check:
        return choice(['I do not understand...','Do you mind rephrasing that?'])

    else:
        return response_by_keyword_check
