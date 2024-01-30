from random import choice, randint
from Validation_Handler import ValidationHandler
from DMV_API_Handler import DMVAPIHandler


validation_handler= ValidationHandler()
dmv_handler = DMVAPIHandler()


def get_response(user_input: str) -> str:
    date_keyword = ["date", "earlier", "dates"]
    distance_keyword = ["miles", "mile"]
    greeting_keyword = ["hello","hi","hey"]
    print("user_input and type", user_input, type(user_input))

    #check user input includes 2 data -> 1.date 3. zipcode
    if_in_keyword = False
    if_date_and_zipcode = False
    split_user_input_list = user_input.lower().split()
    print("split_user_input_list: ",split_user_input_list)
    #if all word in split_user_input_list are numbers
    if validation_handler.check_is_num(split_user_input_list):
        user_input_validation = validation_handler.date_zipcode_input_validation_V2(split_user_input_list)
        if user_input_validation == "pass":
            print("validation pass")
            if_date_and_zipcode = True

    #split_user_input_list includes string
    else:
        print("確認有盡到這裡?" )
        for word in split_user_input_list:

            if word in greeting_keyword:
                print("是不是來到這word", word)
                if_in_keyword = True
                return "Hello there! How can I help you ?"
            elif word in date_keyword:
                if_in_keyword = True
                return f"Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"

            elif word in distance_keyword:
                if_in_keyword = True
                return f"Hey ~ Please provide the date(YYYY-MM-DD) zipcode (i.e. 98087) specific mile(i.e. 7 miles)"

    if not (if_in_keyword or if_date_and_zipcode):
        print("最後答案false")
        # return False
        return choice(['I do not understand...','Do you mind rephrasing that?'])

    # return True
    else:
        print("這裡的條件是 是數字且兩個都有")
        for num in split_user_input_list:
            if validation_handler.check_length_zipcode_input_validtion(num):
                zipcode = int(num)
                return dmv_handler.get_dmv_office_nearby_data_api(zipcode)


# def get_response(user_input: str) -> str:
#     lowered: str = user_input.lower()
#     split_user_input_list = lowered.split()
#     print("split_user_input_list想要發api",split_user_input_list)

#     response_by_keyword_check = check_input_is_number(lowered)
#     print("是因為這裡回應的",response_by_keyword_check)

#     return response_by_keyword_check
