import sys
import requests, datetime
from datetime import datetime



#make datetime formate
def make_datetime_formate(str):
    print("這裡是make_datetime_formate")
    split_str = str.split("-")
    datetime_formate = datetime(int(split_str[0]),int(split_str[1]),int(split_str[2][:2]))
    print(f"---datetime_formate {datetime_formate} {type(datetime_formate)}")
    return datetime_formate

#API -san jose location available dates list
def get_sj_date_data_api():
    url = "https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/516!56b48e272ba45819d81868f440fb30eb6c406b705436cf1d101d2ea2c75c/dates?services[]=DL!b94ae07d48f4d0cff89b6fc0e0c9aea5fa2a47d11728311b7adccdef2c728&numberOfCustomers=1&ver=977125805110.5748"
    response = requests.get(url)

    data = response.json()

    return data[0]


#API -locations available dates list
def get_date_data_api(dmv_field_office_public_id):

    url = f"https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/{dmv_field_office_public_id}/dates?services[]=DL!b94ae07d48f4d0cff89b6fc0e0c9aea5fa2a47d11728311b7adccdef2c728&numberOfCustomers=1&ver=977125805110.5748"
    response = requests.get(url)

    available_datas_data = response.json()
    print(f"確認拿到的 dmv_field_office_public_id {available_datas_data}")

    earliest_available_date = available_datas_data[0]

    return earliest_available_date

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
    return data
    # dmv_office_nearby = []
    # for office in data:
    #     print(f"office {office}")
    #     if office["distance"] < 7:
    #         dmv_office_nearby.append(office)
    # print(f"檢查是否在範圍內7 miles的dmv {dmv_office_nearby}")
    # return dmv_office_nearby




#find the earliest date and add weekday information
def find_earliest_date(formated_input_date,formated_date_from_all_list, office_location):
    old_day = formated_input_date.strftime("%A")
    if formated_date_from_all_list < formated_input_date:

        new_day = formated_date_from_all_list.strftime("%A")
        time_slots= get_time_slot_data_api(formated_date_from_all_list)
        print("---------------------------------------------")

        print(f"The date you have on hand is on {formated_input_date} {old_day}!")

        print(f"I found ONE earlier than what you have!!!!\n Location : {office_location} ,\n Date : {formated_date_from_all_list} {new_day},\n Time slots as followings: ")
        for time_slot in time_slots:
            print(time_slot)
    else:

        return f"Sorry, I can't find earlier one"


#input validation
def input_validation(input_date,input_zipcode):
    print(f"這裡是 input_validation {input_date,input_zipcode} {type(input_date)} and {type(input_zipcode)}")
    if not isinstance(input_date,str):

        return "The input_date should be a string type with YYYY-MM-DD"
    elif not isinstance(input_zipcode, int):

        return "Invalid zipcode"
    else:
        try:
            date_obj = datetime.strptime(input_date, "%Y-%m-%d")

        except ValueError as e:
            return e




#get user input- either a reminder string or input list
def get_input_date_zipcode():
    if len(sys.argv) == 3:
        print(sys.argv)
        input_date = sys.argv[1]
        input_zipcode = int(sys.argv[2])
        validatetion_result = input_validation(input_date,input_zipcode)
        if validatetion_result is not None:
            return validatetion_result
        else:
            return sys.argv
    else:
        return "Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087)"


#get input: date & zipcode
user_input_date_zipcode = get_input_date_zipcode()


#get user input and convert into datatime
if isinstance(user_input_date_zipcode,list):

    #format user input date as datetime
    formated_input_date = make_datetime_formate(user_input_date_zipcode[1])

    #get all nearby dmv offices
    nearby_dmv_offices = get_dmv_office_nearby_data_api(user_input_date_zipcode[2])

    #get earliest date in each nearby dmv offices
    earliest_date_with_office = {}
    for office in nearby_dmv_offices:
        earliest_date= get_date_data_api(office['meta']["dmv_field_office_public_id"])
        print(f"這裡是搜尋後最早的日期 {earliest_date} {type(earliest_date)}")
        earliest_date_with_office[office['slug']] = earliest_date
    print(f"最後結果 {earliest_date_with_office}")

    #convert dates in string type into datetime type
    all_dates_list = list(earliest_date_with_office.values())
    print(f"all_dates_list 長什麼樣子 {all_dates_list} {type(all_dates_list)}")

    for i in range(len(all_dates_list)):
        print(f"改變前:{all_dates_list[i]} and {type(all_dates_list[i])}")
        all_dates_list[i] = make_datetime_formate(all_dates_list[i])

    # for date in all_dates_list:
    #     print(f"改變後:{date} and {type(date)}")

    for i in range(len(all_dates_list)):
        office_location = list(earliest_date_with_office.keys())
        print(find_earliest_date(formated_input_date,all_dates_list[i],office_location[i]))

    # for formated_date_from_all_list in all_dates_list:
    #     print(find_earliest_date(formated_input_date,formated_date_from_all_list))

    # #get the earliest available date from sj location and conver into dattime
    # available_earliest_date_from_sj = get_sj_date_data_api()
    # formated_date_earliest_from_list = make_datetime_formate(available_earliest_date_from_sj)


    # #compare the date you have and availble date to get the earlier date
    # print(find_earliest_date(formated_input_date,formated_date_earliest_from_list))

else:
    # print(user_input_zipcode)
    print(user_input_date_zipcode)
