from random import choice, randint
from Validation_Handler import ValidationHandler
from DMV_API_Handler import DMVAPIHandler
from Date_Handler import DateHandler
import requests, datetime
from datetime import datetime
from Database_Handler import DatabaseHandler
import datetime

validation_handler= ValidationHandler()
dmv_api_handler = DMVAPIHandler()
date_handler = DateHandler()
database_handler= DatabaseHandler()

res = {"response":None, "record":None}




#format response- 
def format_response(user_input_list, nearby_dmv_offices_data):

    #formated_input_date
    for num in user_input_list:
        if validation_handler.check_datetime_formate_validation(num):
            formated_input_date = date_handler.make_string_to_datetime_format(num)



    #iterate through the data to format the res
    for office in nearby_dmv_offices_data:
        #find earliest date in the office
        earliest_available_date= dmv_api_handler.get_date_data_api(office['meta']['dmv_field_office_public_id'])

        office["earliest_available_date"] = date_handler.make_string_to_datetime_format(earliest_available_date)

        information = date_handler.find_earlier_date_than_user_input(formated_input_date, office["earliest_available_date"], office)


        office["information"] = information


    #check each office in nearby_dmv_office_data if it has earlier date
    checked_nearby_dmv_offices_data = []
    for office in nearby_dmv_offices_data:
        if not office["information"].startswith("Sorry"):
            checked_nearby_dmv_offices_data.append(office)

    old_day = formated_input_date.strftime("%A")
    number_of_office = len(checked_nearby_dmv_offices_data)

    msg_to_user = f"The date you have on hand is on {formated_input_date} {old_day}!\n I found {number_of_office} location(s) with earlier time than what you have!\n\n"

    # response = msg_to_user + "\n".join([f"-------------\n{office['information']}\n" for office in checked_nearby_dmv_offices_data]) + "\n you may also provide specific miles (i.e. 7 miles) AND zipcode AND date, the bot will find earlier date within specific miles for you."
    response = msg_to_user + "\n".join([f"-------------\n{office['information']}\n" for office in checked_nearby_dmv_offices_data]) + "\n you may also provide specific miles (i.e. 7 miles) the bot will find earlier date within specific miles for you."

    return response

#改成只有2個params-string
#response by user input, taking organized user input
def get_response(user_input: str,first_time_user =True):
    res = {"response":None, "record":None}

    date_keyword = ["date", "earlier", "dates"]
    distance_keyword = ["miles", "mile"]
    greeting_keyword = ["hello","hi","hey"]

    user_input_datetime =""
    user_input_zipcode =""
    user_input_mile = 0


    #convert user_input to list and lower case
    split_user_input_list = user_input.lower().split()

    
    if not first_time_user:
        #get user_record_datetime, user_record_zipcode, user_record_mile
        user_input_datetime = split_user_input_list[0]
        user_input_zipcode = split_user_input_list[1]
        user_input_mile = int(split_user_input_list[2])

        if user_input_datetime and user_input_zipcode and user_input_mile != 0:
            res["record"] = [user_input_zipcode,user_input_datetime,user_input_mile]
            nearby_dmvs = dmv_api_handler.get_dmv_office_nearby_within_miles_data_api(user_input_zipcode,float(user_input_mile))

            res["response"] = format_response(split_user_input_list,nearby_dmvs)

        # make sure at least datetime and zipcode are provided so that we can store in db
        elif user_input_datetime and user_input_zipcode:

            res["record"] = [user_input_zipcode,user_input_datetime,user_input_mile]
            nearby_dmvs = dmv_api_handler.get_dmv_office_nearby_data_api(user_input_zipcode)

            res["response"] = format_response(split_user_input_list,nearby_dmvs)

    else:
        
        #iterate through list to check each word if it matches zipcode or datetime format
        #user might input: hello, 95035, 20240909
        for word in split_user_input_list:
            if validation_handler.check_convert_into_num(word) and validation_handler.check_length_zipcode_input_validtion(word):

                user_input_zipcode = word
            elif validation_handler.check_datetime_formate_validation(word):

                user_input_datetime = word
        
        #check if user input are valid datetime and valid zipcode,store in res["record"]
        if user_input_datetime and user_input_zipcode:
            res["record"] = [user_input_zipcode,user_input_datetime]
            nearby_dmvs = dmv_api_handler.get_dmv_office_nearby_data_api(user_input_zipcode)

            res["response"] = format_response(split_user_input_list,nearby_dmvs)


        else:
            #ｃheck if the word is in the keyword to send the corresponding response
            for word in split_user_input_list:

                if word in greeting_keyword:
                    res["response"]= "Hello there! How can I help you ?"
                    break

                elif word in date_keyword:
                    res["response"]= "Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"
                    break

                elif word in distance_keyword:
                    res["response"]= "Hey ~ Please provide the date(YYYY-MM-DD) zipcode (i.e. 98087) specific mile(i.e. 7 miles)"
                    break

                else:
                    res["response"]= "sorry i don't understand....you may provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date near you"
            
    return res
