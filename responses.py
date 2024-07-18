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

res = {"response":None, "record":None}


database_handler= DatabaseHandler()
date_handler = DateHandler()



#format response
def format_response(user_input, nearby_dmv_offices_data):
    print("這裡是format response: ",user_input, nearby_dmv_offices_data)

    #formated_input_date
    for num in user_input:
        if validation_handler.check_datetime_formate_validation(num):
            formated_input_date = date_handler.make_string_to_datetime_format(num)
    print("這裡是formated_input_date: ",formated_input_date)
    


    #iterate through the data to format the res
    for office in nearby_dmv_offices_data:
        print("office: ",office)
        #find earliest date in the office
        earliest_available_date= dmv_api_handler.get_date_data_api(office['meta']['dmv_field_office_public_id'])
        print("確認是否有找到可以的時段？ ",earliest_available_date, type(earliest_available_date))
        office["earliest_available_date"] = date_handler.make_string_to_datetime_format(earliest_available_date)

        information = date_handler.find_earlier_date_than_user_input(formated_input_date, office["earliest_available_date"], office)


        print("確認是否有找到information？ ",information)

        office["information"] = information
        print("整理後的office: ",office)

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


#response by user input
def get_response(message,user_input: str,first_time_user =True):
    print("這裡是get_response的message： ",message,user_input)
    res = {"response":None, "record":None}
    date_keyword = ["date", "earlier", "dates"]
    distance_keyword = ["miles", "mile"]
    greeting_keyword = ["hello","hi","hey"]
    no_record_keyword = "theres no previous record"
    user_input_datetime =""
    user_input_zipcode =""
    user_input_mile =""



    #check if user input are all string, and check if it exsits in keyword
    split_user_input_list = user_input.lower().split()
    print("get_response正在running...-get response function 裡面 將user input轉乘小寫後: ", split_user_input_list)

    #是否為first_time_user?
    #若不是first_time_user, 調出db裡面搜尋紀錄,填入有的欄位,幫忙找尋一次again,

    if not first_time_user:
        print("user 之前找過了,調資料出來在幫忙找一次")
        user_input_datetime = split_user_input_list[0]
        user_input_zipcode = split_user_input_list[1]
        #若長度>2,代表user 有input其他資料,確認是不是數字
        if len(split_user_input_list) > 2 and validation_handler.check_convert_into_num(split_user_input_list[2]):
            user_input_mile = split_user_input_list[2]


        if user_input_datetime and user_input_zipcode and user_input_mile:
            # res["response"]= "let me check it for you if there's earlier date than the date you are looking for...."
            res["record"] = [user_input_zipcode,user_input_datetime,user_input_mile]
            nearby_dmvs = dmv_api_handler.get_dmv_office_nearby_within_miles_data_api(user_input_zipcode,float(user_input_mile))
            print(f"找到附近的dmv 在{user_input_mile}mile內:", nearby_dmvs)
            res["response"] = format_response(split_user_input_list,nearby_dmvs)
            print("user提供了datetime and zipcode 並且找到更早的日期： ",format_response(split_user_input_list,nearby_dmvs))
        elif user_input_datetime and user_input_zipcode:
            # res["response"]= "let me check it for you if there's earlier date than the date you are looking for...."
            res["record"] = [user_input_zipcode,user_input_datetime]
            nearby_dmvs = dmv_api_handler.get_dmv_office_nearby_data_api(user_input_zipcode)
            print("找到附近的dmv:", nearby_dmvs)
            res["response"] = format_response(split_user_input_list,nearby_dmvs)
            print("user提供了datetime and zipcode 並且找到更早的日期： ",format_response(split_user_input_list,nearby_dmvs))

    else:


        #iterate through word 確認是否有數字？ 和 datetime?
            #有數字？是否為valid的zipcode格式？
            #有datetime？是否為valid的datetime格式？
        #是否在keyword裡面？
        #若沒有數字也沒有datetime ,也不在keyword裡面 就回答不知道
        for word in split_user_input_list:
            if validation_handler.check_convert_into_num(word) and validation_handler.check_length_zipcode_input_validtion(word):
                print("user input 裡面的word可以轉成數字,並valid zipcode格式")
                user_input_zipcode = word
            elif validation_handler.check_datetime_formate_validation(word):
                print("user input 裡面的word可以轉成datetime,並valid dattime格式")

                user_input_datetime = word
        
        #check if user input valid datetime and valid zipcode,存到db
        if user_input_datetime and user_input_zipcode:
            # res["response"]= "let me check it for you if there's earlier date than the date you are looking for...."
            res["record"] = [user_input_zipcode,user_input_datetime]
            nearby_dmvs = dmv_api_handler.get_dmv_office_nearby_data_api(user_input_zipcode)
            print("找到附近的dmv :", nearby_dmvs)
            res["response"] = format_response(split_user_input_list,nearby_dmvs)
            print("user提供了datetime and zipcode 並且找到更早的日期： ",format_response(split_user_input_list,nearby_dmvs))

        else:
            #是否在keyword裡面？
            for word in split_user_input_list:

                if word in greeting_keyword:
                    # return "Hello there! How can I help you ?"
                    res["response"]= "Hello there! How can I help you ?"
                    break

                elif word in date_keyword:
                    print("user input 裡面的word是打招呼")
                    # return f"Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"
                    res["response"]= "Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"
                    break
                elif word in distance_keyword:
                    print("user input 裡面的word是問距離")

                    # return f"Hey ~ Please provide the date(YYYY-MM-DD) zipcode (i.e. 98087) specific mile(i.e. 7 miles)"
                    res["response"]= "Hey ~ Please provide the date(YYYY-MM-DD) zipcode (i.e. 98087) specific mile(i.e. 7 miles)"
                    break
                else:
                    print("user input 裡面的word 沒有明確說明 無法判斷")

                    res["response"]= "sorry i don't understand....you may provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"
            
    return res


##保留前面的紀錄
# #response by user input
# def get_response(message,user_input: str):
#     res = {"response":None, "record":None}
#     date_keyword = ["date", "earlier", "dates"]
#     distance_keyword = ["miles", "mile"]
#     greeting_keyword = ["hello","hi","hey"]
#     no_record_keyword = "theres no previous record"

#     #check user input includes two datas -> 1.date 3. zipcode
#     if_in_keyword = False
#     if_date_and_zipcode = False
#     split_user_input_list = user_input.lower().split()
#     print("get_response正在running...-get response function 裡面 將user input轉乘小寫後: ", split_user_input_list)


#     input_zipcode = None
#     input_datetime = None
#     mile_range = None

#     # valid_date_zipcode = validation_handler.check_zipcode_datetime_provided_and_valid(split_user_input_list)

#     #if all word in split_user_input_list are numbers
#     if validation_handler.check_is_num(split_user_input_list) and valid_date_zipcode != None:
#         valid_date_zipcode = validation_handler.check_zipcode_datetime_provided_and_valid(split_user_input_list)

#         print("處理要怎麼回應,如果user input都是數字")
#         if_date_and_zipcode = True
#         input_zipcode = valid_date_zipcode[0]
#         input_datetime = valid_date_zipcode[1]
#         cursor = database_handler.get_db_cursor()
#         print("check if cursor is still alive: ",cursor)
#     #split_user_input_list includes string
#     else:
#         print("處理要怎麼回應,如果user input有數字 有string")


#         #check if date and zipcode are provided
#         if valid_date_zipcode!= None:
#             input_zipcode = valid_date_zipcode[0]
#             input_datetime = valid_date_zipcode[1]
#             if_date_and_zipcode = True
#         #check if there's no record
#         if split_user_input_list == no_record_keyword:
#             print("相等沒有任何record紀錄 不知道要怎麼幫忙")
#             if_in_keyword = True
#             res["response"]= "Hello there! How can I help you ?"
#             return res

#         for word in split_user_input_list:
#             #find the miles information
#             mile_range = validation_handler.find_mile_range(split_user_input_list)
#             print("處理後的mileage: ", mile_range)

#             if mile_range and input_datetime and input_zipcode:
#                 dmv_office_within_miles_data = dmv_api_handler.get_dmv_office_nearby_within_miles_data_api(input_zipcode, int(mile_range))
#                 # return format_response(split_user_input_list,dmv_office_within_miles_data)
#                 res["response"] = format_response(split_user_input_list,dmv_office_within_miles_data)
#                 res["record"] = {"zipcode": input_zipcode,"datetime": input_datetime,"mile_range": mile_range}
#                 print("3個都有資料-zipcode datetime mile_range: ", mile_range)
#                 return res
#             elif word in greeting_keyword:
#                 if_in_keyword = True
#                 # return "Hello there! How can I help you ?"
#                 res["response"]= "Hello there! How can I help you ?"
#                 return res
#             elif word in date_keyword:
#                 if_in_keyword = True
#                 # return f"Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"
#                 res["response"]= "Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you"
#                 return res
#             elif word in distance_keyword:
#                 if_in_keyword = True
#                 # return f"Hey ~ Please provide the date(YYYY-MM-DD) zipcode (i.e. 98087) specific mile(i.e. 7 miles)"
#                 res["response"]= "Hey ~ Please provide the date(YYYY-MM-DD) zipcode (i.e. 98087) specific mile(i.e. 7 miles)"
#                 return res



#     #checking if is valid user input
#     #if not in keyword lists OR not valid date and zipcode
#     if not (if_in_keyword or if_date_and_zipcode):
#         print("get_response-zipcode 和dates只提供其中一個")

#         # res["response"]=choice(['I do not understand... How can I help you?','Do you mind rephrasing that? How can I help you?'])
#         res["response"]= 'Do you mind rephrasing that? How can I help you?'

#         return res

#     #if both numbers- zipcode and dates are provided
#     else:
#         print("get_response-zipcode 和dates都由提供")
#         for num in split_user_input_list:
#             if validation_handler.check_length_zipcode_input_validtion(num):
#                 zipcode = int(num)
#                 nearby_dmv_offices_data =  dmv_api_handler.get_dmv_office_nearby_data_api(zipcode)
#                 #format response data AND related record
#                 # return format_response(split_user_input_list,nearby_dmv_offices_data)
#                 res["response"] = format_response(split_user_input_list,nearby_dmv_offices_data)
#                 res["record"] = {"zipcode": input_zipcode,"datetime": input_datetime,"mile_range": mile_range}
#                 return res
