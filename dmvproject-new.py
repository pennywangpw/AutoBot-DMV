import sys
import requests, datetime
from datetime import datetime
from gmailtest import send_email
from discord_bot_webhook import send_notification_through_discord
import discord
from discord_bot import bot
from api import get_sj_date_data_api,get_date_data_api,get_time_slot_data_api,get_dmv_office_nearby_data_api
from shared_data import nearby_dmv_offices

#interactive bot
TOKEN = 'MTE4NjQyNDc1MDcyNjIwNTQ1MQ.GHRAcH.zpeMJCrMf02WYJVgevvhMFBtgKPbgWV48fvJaM'


#make datetime formate
def make_datetime_formate(str):
    split_str = str.split("-")
    datetime_formate = datetime(int(split_str[0]),int(split_str[1]),int(split_str[2][:2]))
    return datetime_formate


#find the earliest date and add weekday information
def find_earlier_date_than_user_input(formated_input_date,formated_date_from_all_list, office_obj):
    old_day = formated_input_date.strftime("%A")
    if formated_date_from_all_list < formated_input_date:

        new_day = formated_date_from_all_list.strftime("%A")

        dmv_field_office_public_id = office_obj['meta']['dmv_field_office_public_id']
        time_slots= get_time_slot_data_api(dmv_field_office_public_id,formated_date_from_all_list)

        print("---------------------------------------------")

        available_time_slots = []

        for time_slot in time_slots:
            available_time_slots.append(time_slot)

        time_slots_str = '\n'.join(available_time_slots)
        information = f"Id: {office_obj['id']} \n Location : {office_obj['slug']},\n Date : {formated_date_from_all_list} {new_day},\n Time slots as followings: \n{time_slots_str}"
        return information

    else:

        return f"Sorry, I can't find earlier one at {office_obj['id']} {office_obj['slug']}"


#input validation
def input_validation(input_date,input_zipcode):
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
        input_date = sys.argv[1]
        input_zipcode = int(sys.argv[2])
        validatetion_result = input_validation(input_date,input_zipcode)
        if validatetion_result is not None:
            return validatetion_result
        else:
            return sys.argv
    else:
        return "Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087)"



#測試bot
# Check if the bot is ready
@bot.event
async def on_ready():
    print(f'Bot is ready: {bot.user.name} ({bot.user.id})')

# Example: Send a message to trigger the !update command
async def send_update_command():
    # Create a context with a fake message
    ctx = await bot.get_context(discord.Message(content='!send_notification'))

    # Invoke the !update command
    await bot.invoke(ctx)

# Run the bot
bot.run(TOKEN)



#GOAL: 我想要信件可以收到一封就好,一封包含所有available ealier time

#get input: date & zipcode
user_input_date_zipcode = get_input_date_zipcode()


#get user input and convert into datatime
if isinstance(user_input_date_zipcode,list):

    #format user input date as datetime
    formated_input_date = make_datetime_formate(user_input_date_zipcode[1])

    #get all nearby dmv offices
    nearby_dmv_offices_data = get_dmv_office_nearby_data_api(user_input_date_zipcode[2])


    #add attribute - 1. earliest_available_date in each nearby_dmv_offices_data & 2. information with find_earlier_date_than_user_input information
    for office in nearby_dmv_offices_data:
        earliest_date= get_date_data_api(office['meta']["dmv_field_office_public_id"])
        office["earliest_available_date"] = make_datetime_formate(earliest_date)
        information = find_earlier_date_than_user_input(formated_input_date,office["earliest_available_date"],office)
        office["information"] = information
        nearby_dmv_offices.append(office)



    #send an email with all avilable ealier time with locations information
    send_email(formated_input_date,nearby_dmv_offices_data)
    send_notification_through_discord(formated_input_date,nearby_dmv_offices_data)




else:
    # print(user_input_zipcode)
    print(user_input_date_zipcode)
