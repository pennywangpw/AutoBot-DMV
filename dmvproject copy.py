import sys
import requests, datetime
from datetime import datetime



#make datetime formate
def make_datetime_formate(str):
    print("這裡是make_datetime_formate")
    split_str = str.split("-")
    datetime_formate = datetime(int(split_str[0]),int(split_str[1]),int(split_str[2][:2]))
    print(f"---datetime_formate {datetime_formate}")
    return datetime_formate

#API -san jose location available dates list
def get_sj_date_data_api():
    url = "https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/516!56b48e272ba45819d81868f440fb30eb6c406b705436cf1d101d2ea2c75c/dates?services[]=DL!b94ae07d48f4d0cff89b6fc0e0c9aea5fa2a47d11728311b7adccdef2c728&numberOfCustomers=1&ver=977125805110.5748"
    response = requests.get(url)

    data = response.json()

    return data[0]


#API- find available time slot
def get_time_slot_data_api(datetime):

    date = datetime.strftime("%Y-%m-%d")

    url = f"https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/516!56b48e272ba45819d81868f440fb30eb6c406b705436cf1d101d2ea2c75c/times?date={date}&services[]=DL!b94ae07d48f4d0cff89b6fc0e0c9aea5fa2a47d11728311b7adccdef2c728&numberOfCustomers=1&ver=867712719559.5795"

    response = requests.get(url)

    data = response.json()

    return data

#API- find nearby DMV office by zipcode
def get_dmv_office_nearby_data_api(zipcode):

    url = f"https://www.dmv.ca.gov/portal/wp-json/dmv/v1/field-offices?q={zipcode}"
    response = requests.get(url)
    data = response.json()

    dmv_office_nearby = []
    for office in data:
        print(f"office {office}")
        if office["distance"] < 7:
            dmv_office_nearby.append(office)
    print(f"檢查是否在範圍內的dmv {dmv_office_nearby}")
    return dmv_office_nearby




#find the earliest date and add weekday information
def find_earliest_date(input_date,available_date_from_list):
    old_day = input_date.strftime("%A")
    if available_date_from_list < input_date:

        new_day = available_date_from_list.strftime("%A")
        time_slots= get_time_slot_data_api(available_date_from_list)
        print(f"I found ONE earlier than what you have!!!!  The new date is on {available_date_from_list} {new_day} and time slots as followings: ")
        for time_slot in time_slots:
            print(time_slot)
        return f"Just for your reference - The date you have on hand is on {input_date} {old_day}!"
    else:

        return f"Sorry, I can't find earlier one"


#input validation
def input_validation(input):

    if not isinstance(input,str):
        return "The input should be a string type with YYYY-MM-DD"
    else:
        try:
            date_obj = datetime.strptime(input, "%Y-%m-%d")

        except ValueError as e:
            return e




#get user input- either a reminder string or input list
def get_input_date():
    if len(sys.argv) > 1:
        print(sys.argv)
        input_date = sys.argv[1]
        validatetion_result = input_validation(input_date)
        if validatetion_result is not None:
            return validatetion_result
        else:
            return sys.argv
    else:
        return "Please provide the date you have (YYYY-MM-DD)"






get_dmv_office_nearby_data_api(95035)
user_input_date = get_input_date()



#get user input and convert into datatime, what date they have been booked?
# user_input_date = input("Find the earlier date than what I have on hand? ")
if isinstance(user_input_date,list):


    formated_input_date = make_datetime_formate(user_input_date[1])



    #get the earliest available date from sj location and conver into dattime
    available_earliest_date_from_sj = get_sj_date_data_api()
    formated_date_earliest_from_list = make_datetime_formate(available_earliest_date_from_sj)


    #compare the date you have and availble date to get the earlier date
    print(find_earliest_date(formated_input_date,formated_date_earliest_from_list))

else:
    print(user_input_date)
