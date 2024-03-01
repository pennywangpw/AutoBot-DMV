from random import choice, randint
from Validation_Handler import ValidationHandler
from DMV_API_Handler import DMVAPIHandler
from Date_Handler import DateHandler
import requests, datetime
from datetime import datetime

validation_handler= ValidationHandler()
dmv_api_handler = DMVAPIHandler()
date_handler = DateHandler()


#compare user input date and earliest available date in zipcode area to find the earlier date
def find_earliest_date(formated_input_date,formated_date_from_all_list, office_obj):
    return date_handler.find_earlier_date_than_user_input(formated_input_date,formated_date_from_all_list, office_obj)

#format response
def format_response(user_input, nearby_dmv_offices_data):

    #formated_input_date
    for num in user_input:
        if validation_handler.check_datetime_formate_validation(num):
            formated_input_date = date_handler.make_string_to_datetime_formate(num)


    #iterate through the data to format the res
    for office in nearby_dmv_offices_data:
        #find earliest date in the office
        earliest_available_date= dmv_api_handler.get_date_data_api(office['meta']['dmv_field_office_public_id'])
        office["earliest_available_date"] = date_handler.make_datetime_formate(earliest_available_date)

        information = find_earliest_date(formated_input_date,office["earliest_available_date"],office)
        office["information"] = information

    #check each office in nearby_dmv_office_data if it has earlier date
    checked_nearby_dmv_offices_data = []
    for office in nearby_dmv_offices_data:
        if not office["information"].startswith("Sorry"):
            checked_nearby_dmv_offices_data.append(office)

    old_day = formated_input_date.strftime("%A")
    number_of_office = len(checked_nearby_dmv_offices_data)

    msg_to_user = f"The date you have on hand is on {formated_input_date} {old_day}!\n I found {number_of_office} location(s) with earlier time than what you have!\n\n"

    response = msg_to_user + "\n".join([f"-------------\n{office['information']}\n" for office in checked_nearby_dmv_offices_data]) + "\n you may also provide specific miles (i.e. 7 miles) AND zipcode AND date, the bot will find earlier date within specific miles for you."
    print("我的response: ",response)
    return response




#response by user input
def get_response(user_input: str) -> str:
    date_keyword = ["date", "earlier", "dates"]
    distance_keyword = ["miles", "mile"]
    greeting_keyword = ["hello","hi","hey"]

    #check user input includes 2 data -> 1.date 3. zipcode
    if_in_keyword = False
    if_date_and_zipcode = False
    split_user_input_list = user_input.lower().split()
    print("split_user_input_list: ",split_user_input_list)


    input_zipcode = None
    input_datetime = None
    mile_range = None

    #if all word in split_user_input_list are numbers
    if validation_handler.check_is_num(split_user_input_list) and validation_handler.check_zipcode_datetime_provided_and_valid(split_user_input_list) != None:
        if_date_and_zipcode = True

    #split_user_input_list includes string
    else:

        #find the miles information
        for word in split_user_input_list:
            #check if word is about miles
            mile_range = validation_handler.find_mile_range(word)
            break

        #check if date and zipcode are provided
        if validation_handler.check_zipcode_datetime_provided_and_valid(split_user_input_list)!= None:
            input_zipcode = validation_handler.check_zipcode_datetime_provided_and_valid(split_user_input_list)[0]
            input_datetime = validation_handler.check_zipcode_datetime_provided_and_valid(split_user_input_list)[1]
            if_date_and_zipcode = True


        if mile_range and if_date_and_zipcode:
            dmv_office_within_miles_data = dmv_api_handler.get_dmv_office_nearby_within_miles_data_api(input_zipcode, int(mile_range))
            return format_response(split_user_input_list,dmv_office_within_miles_data)
        elif word in greeting_keyword:
            if_in_keyword = True
            return "Hello there! How can I help you ?"
        elif word in date_keyword:
            if_in_keyword = True
            return f"Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"

        elif word in distance_keyword:
            if_in_keyword = True
            return f"Hey ~ Please provide the date(YYYY-MM-DD) zipcode (i.e. 98087) specific mile(i.e. 7 miles)"



    #checking if is valid user input
    #if not in keyword lists OR not valid date and zipcode
    if not (if_in_keyword or if_date_and_zipcode):
        return choice(['I do not understand...','Do you mind rephrasing that?'])

    #if both numbers- zipcode and dates are provided
    else:
        for num in split_user_input_list:
            if validation_handler.check_length_zipcode_input_validtion(num):
                zipcode = int(num)
                nearby_dmv_offices_data =  dmv_api_handler.get_dmv_office_nearby_data_api(zipcode)
                #format response data
                return format_response(split_user_input_list,nearby_dmv_offices_data)

    # #if all word in split_user_input_list are numbers
    # if validation_handler.check_is_num(split_user_input_list):
    #     for word in split_user_input_list:
    #         if validation_handler.check_length_zipcode_input_validtion(word):
    #             input_zipcode = word
    #         elif validation_handler.check_datetime_formate_validation(word):
    #             input_datetime = word

    #     if input_zipcode != None and input_datetime != None:
    #         if_date_and_zipcode = True

    # #split_user_input_list includes string
    # else:
    #     print("確認有到這裡?" )
    #     #find the miles information
    #     for word in split_user_input_list:
    #         #check if word is about miles
    #         mile_range = validation_handler.find_mile_range(word)
    #         print("拿到什麼mile_range: ", mile_range)
    #         break

    #     #find zipcode and datetime information
    #     for word in split_user_input_list:
    #         if validation_handler.check_length_zipcode_input_validtion(word):
    #             input_zipcode = word
    #         elif validation_handler.check_datetime_formate_validation(word):
    #             input_datetime = word

    #     if input_zipcode != None and input_datetime != None:
    #         if_date_and_zipcode = True


    #     if mile_range and if_date_and_zipcode:
    #         dmv_office_within_miles_data = dmv_api_handler.get_dmv_office_nearby_within_miles_data_api(input_zipcode, int(mile_range))
    #         return format_response(split_user_input_list,dmv_office_within_miles_data)
    #     elif word in greeting_keyword:
    #         if_in_keyword = True
    #         return "Hello there! How can I help you ?"
    #     elif word in date_keyword:
    #         if_in_keyword = True
    #         return f"Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"

    #     elif word in distance_keyword:
    #         if_in_keyword = True
    #         return f"Hey ~ Please provide the date(YYYY-MM-DD) zipcode (i.e. 98087) specific mile(i.e. 7 miles)"



    # #checking if is valid user input
    # #if not in keyword lists OR not valid date and zipcode
    # if not (if_in_keyword or if_date_and_zipcode):
    #     return choice(['I do not understand...','Do you mind rephrasing that?'])

    # #if both numbers- zipcode and dates are provided
    # else:
    #     for num in split_user_input_list:
    #         if validation_handler.check_length_zipcode_input_validtion(num):
    #             zipcode = int(num)
    #             nearby_dmv_offices_data =  dmv_api_handler.get_dmv_office_nearby_data_api(zipcode)
    #             #format response data
    #             return format_response(split_user_input_list,nearby_dmv_offices_data)
