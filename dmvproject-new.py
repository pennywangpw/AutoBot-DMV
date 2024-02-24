import sys
import requests, datetime
from datetime import datetime
# from gmailtest import send_email
from Email_Handler import EmailHandler
from discord_bot_webhook import send_notification_through_discord
import discord
from DMV_API_Handler import DMVAPIHandler
from Date_Handler import DateHandler
from discord.ext import commands
from Validation_Handler import ValidationHandler
import random
import string


#interactive bot



dmv_api_handler = DMVAPIHandler()
email_handler = EmailHandler()
date_handler = DateHandler()
validation_handler= ValidationHandler()



#active bot
def active_robot():
    print(f"輸入內容{sys.argv}")
    if "active" in sys.argv:
        print("bot is ready to communicate with the user....")
        return True
    else:
        print("bot is not ready yet....")
        return False


# response- format response
def format_response(formated_input_date, nearby_dmv_offices_data):
    print(f"檢查一下傳進來的 format_response {formated_input_date, nearby_dmv_offices_data} ")
    #check each office in nearby_dmv_office_data if it has earlier date
    checked_nearby_dmv_offices_data = []
    for office in nearby_dmv_offices_data:
        if not office["information"].startswith("Sorry"):
            checked_nearby_dmv_offices_data.append(office)

    old_day = formated_input_date.strftime("%A")
    number_of_office = len(checked_nearby_dmv_offices_data)

    msg_to_user = f"The date you have on hand is on {formated_input_date} {old_day}!\n I found {number_of_office} location(s) with earlier time than what you have!\n\n"

    response = msg_to_user + "\n".join([f"-------------\n{office['information']}\n" for office in checked_nearby_dmv_offices_data]) + "\n you may also provide specific miles (i.e. 7 miles) AND zipcode AND date, the bot will find earlier date within specific miles for you."
    return response


# response - format response within specific distance
def format_response_within_d(formated_input_date, nearby_dmv_offices_data):
    print(f"檢查一下傳進來的 format_response {formated_input_date, nearby_dmv_offices_data} ")
    #check each office in nearby_dmv_office_data if it has earlier date
    checked_nearby_dmv_offices_data = []
    for office in nearby_dmv_offices_data:
        if not office["information"].startswith("Sorry"):
            checked_nearby_dmv_offices_data.append(office)

    old_day = formated_input_date.strftime("%A")
    number_of_office = len(checked_nearby_dmv_offices_data)

    msg_to_user = f"The date you have on hand is on {formated_input_date} {old_day}!\n I found {number_of_office} location(s) with earlier time than what you have!\n\n"

    response = msg_to_user + "\n".join([f"-------------\n{office['information']}\n" for office in checked_nearby_dmv_offices_data])
    return response

#remove punctuation marks
def remove_punctuation(user_input_string):
    translator = str.maketrans('', '', string.punctuation)
    result = user_input_string.translate(translator)
    return result



#GOAL: 將啟動和互動的部分拆開

#get input: date & zipcode
robot_is_active = active_robot()


if robot_is_active:
    bot = commands.Bot(command_prefix="", intents=discord.Intents.all())

    #不需要透過command name 當Event發生時可以直接執行
    # Bot is ready and ask first question
    @bot.event
    async def on_ready():
        print(f"Hello Penny! Bot is ready for you...")
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send("The bot is online.\nPlease provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you")

    # Bot will respond the user by keywords
    @bot.event
    async def on_message(message):
        # check if bot is not responding itself
        if message.author == bot.user:
            return

        #list of keywords
        date_keyword = ["date", "earlier", "dates"]
        distance_keyword = ["miles", "mile"]
        # zipcode_keyword = dmv_api_handler.get_dmv_offices_zipcode_data_api()


        #lower and split user input sentense in a list
        message_content_remove_punctuation= remove_punctuation(message.content)
        message_text = message_content_remove_punctuation.lower().split()



        # input_validation= validation_handler.date_zipcode_input_validation_V2(message_text)
        # print(f"input_validation {input_validation}")
        # if input_validation == "pass":
        mile = None
        zipcode = None
        input_date = None

        #iterate through each word from user input to check if any word in distance_keyword
        for i in range (len(message_text)): #[10 miles] [20240130 95035]
            word = message_text[i]
            if word in distance_keyword:
                mile = message_text[i-1]
            #check if the word is zipcode
            elif validation_handler.check_convert_into_num(word) and validation_handler.check_length_zipcode_input_validtion(word):
                zipcode = int(word)
            elif validation_handler.check_datetime_formate_validation(word):
                input_date = word


        if mile is not None and zipcode is not None and input_date is not None:
            #convert date string into datetime
            #find nearby dmv offices
            formated_date = date_handler.make_string_to_datetime_formate(input_date)
            nearby_dmv_offices_data = dmv_api_handler.get_dmv_office_nearby_within_miles_data_api(zipcode,int(mile))

            for office in nearby_dmv_offices_data:
                earliest_available_date= dmv_api_handler.get_date_data_api(office['meta']['dmv_field_office_public_id'])
                office["earliest_available_date"] = date_handler.make_datetime_formate(earliest_available_date)
                information = date_handler.find_earlier_date_than_user_input(formated_date,office["earliest_available_date"],office)
                office["information"] = information

            await message.channel.send(format_response_within_d(formated_date,nearby_dmv_offices_data))

        #if the user input zipcode and date
        elif zipcode is not None and input_date is not None:
            formated_date = date_handler.make_string_to_datetime_formate(input_date)

            nearby_dmv_offices_data = dmv_api_handler.get_dmv_office_nearby_data_api(zipcode)

            #iterate nearby_dmv_offices_date to get earliest available date in each office (create earliest_available_date attribute to collect result)
            #check earliest available date if ealier than user input date (create information attribute to collect info)
            for office in nearby_dmv_offices_data:
                earliest_available_date= dmv_api_handler.get_date_data_api(office['meta']['dmv_field_office_public_id'])
                office["earliest_available_date"] = date_handler.make_datetime_formate(earliest_available_date)
                information = date_handler.find_earlier_date_than_user_input(formated_date,office["earliest_available_date"],office)
                office["information"] = information


            await message.channel.send(format_response(formated_date,nearby_dmv_offices_data))

        else:
            await message.channel.send("oh! NOT PASS VALIDATION. This is invalid input.\nPlease provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087)")





    bot.run(TOKEN)

else:
    print("Sorry, bot is not ready yet....")
