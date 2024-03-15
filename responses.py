from random import choice, randint
from Validation_Handler import ValidationHandler
from DMV_API_Handler import DMVAPIHandler
from Date_Handler import DateHandler
import requests, datetime
from datetime import datetime

validation_handler= ValidationHandler()
dmv_api_handler = DMVAPIHandler()
date_handler = DateHandler()

data = {"response":None, "record":None}


#compare user input date and earliest available date in zipcode area to find the earlier date
def find_earliest_date(formated_input_date,formated_date_from_all_list, office_obj):
    return date_handler.find_earlier_date_than_user_input(formated_input_date,formated_date_from_all_list, office_obj)

#format response
def format_response(user_input, nearby_dmv_offices_data):
    print("這是送進format_response的內容: ",user_input)

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

    # response = msg_to_user + "\n".join([f"-------------\n{office['information']}\n" for office in checked_nearby_dmv_offices_data]) + "\n you may also provide specific miles (i.e. 7 miles) AND zipcode AND date, the bot will find earlier date within specific miles for you."
    response = msg_to_user + "\n".join([f"-------------\n{office['information']}\n" for office in checked_nearby_dmv_offices_data]) + "\n you may also provide specific miles (i.e. 7 miles) the bot will find earlier date within specific miles for you."

    print("我的response: ",response)
    return response




#response by user input, return string
def get_response(user_input: str):
    global data

    #keyword list
    date_keyword = ["date", "earlier", "dates"]
    distance_keyword = ["miles", "mile"]
    greeting_keyword = ["hello","hi","hey"]


    #convert user_input to lowercase and split it in a list
    split_user_input_list = user_input.lower().split()
    print("get response function 裡面 將user input轉乘小寫後: ", split_user_input_list)


    input_zipcode = None
    input_datetime = None
    mile_range = None

    #find mile range
    mile_range = validation_handler.find_mile_range(split_user_input_list)

    #can find zipcode AND datetime
    if validation_handler.check_zipcode_datetime_provided_and_valid(split_user_input_list) and not mile_range:
        print("0000 可以找到 zipcode AND datetime 但找不到mile: ",mile_range)

        #find zipcode and datetime
        input_zipcode = validation_handler.check_zipcode_datetime_provided_and_valid(split_user_input_list)[0]
        input_datetime = validation_handler.check_zipcode_datetime_provided_and_valid(split_user_input_list)[1]

        #API
        nearby_dmv_offices_data =  dmv_api_handler.get_dmv_office_nearby_data_api(input_zipcode)

        #format response data AND update data
        data["response"] = format_response(split_user_input_list,nearby_dmv_offices_data)
        data["record"] = {"zipcode": input_zipcode,"datetime": input_datetime,"mile_range": mile_range}
        print("這裡是有input_zipcode and input_datetime 後的data: ", data)
        return data

    #can find zipcode AND datetime AND mile_range
    elif validation_handler.check_zipcode_datetime_provided_and_valid(split_user_input_list) and mile_range:
        print("0000 可以找到 zipcode AND datetime AND mile_range")

        #find zipcode and datetime
        input_zipcode = validation_handler.check_zipcode_datetime_provided_and_valid(split_user_input_list)[0]
        input_datetime = validation_handler.check_zipcode_datetime_provided_and_valid(split_user_input_list)[1]



        #API
        print("送進api的mile_range type: ", mile_range, type(mile_range))
        dmv_office_within_miles_data = dmv_api_handler.get_dmv_office_nearby_within_miles_data_api(input_zipcode, mile_range)

        #format response data AND update data
        data["response"] = format_response(split_user_input_list,dmv_office_within_miles_data)
        data["record"] = {"zipcode": input_zipcode,"datetime": input_datetime,"mile_range": mile_range}
        print("這裡是有mile_range and input_zipcode and input_datetime 後的data: ", data)
        return data

    else:
        print("0000 不可以找到 zipcode AND datetime ")

        #check if all word in split_user_input_list are numbers
        if validation_handler.check_is_num(split_user_input_list):
            print("^^^^^^^這裡是落入 不可以找到 zipcode AND datetime user_input都是數字: ",split_user_input_list)

            #update data
            data["response"]= 'Do you mind rephrasing that? How can I help you?'
            print("這裡是沒有給齊 zipcode and datatime 的data: ", data)

            return data


        #split_user_input_list includes string
        else:
            print("^^^^^^^這裡是落入 不可以找到 zipcode AND datetime user_input有文字: ",split_user_input_list)

            #check if split_user_input_list includes any word in keyword
            for word in split_user_input_list:
                print("^^^^^^^不可以找到 zipcode AND datetime, user_input有文字 檢查後有在keyword中可以回復: ")

                if word in greeting_keyword:
                    # return "Hello there! How can I help you ?"
                    data["response"]= "Hello there! How can I help you ?"
                    return data
                elif word in date_keyword:
                    # return f"Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"
                    data["response"]= "Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"
                    return data
                elif word in distance_keyword:
                    # return f"Hey ~ Please provide the date(YYYY-MM-DD) zipcode (i.e. 98087) specific mile(i.e. 7 miles)"
                    data["response"]= "Hey ~ Please provide the date(YYYY-MM-DD) zipcode (i.e. 98087) specific mile(i.e. 7 miles)"
                    return data


            else:
                data["response"]= 'Do you mind rephrasing that? How can I help you?'
                print("^^^^^^^不可以找到 zipcode AND datetime ,user_input有文字 檢查後不在 keyword中: ",data)
                return data
