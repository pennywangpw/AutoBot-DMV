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
import random


#interactive bot

# CHANNEL_ID = 1186427997851488266


dmv_api_handler = DMVAPIHandler()
email_handler = EmailHandler()
date_handler = DateHandler()



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

#format response
def format_response(formated_input_date, nearby_dmv_offices_data):
    old_day = formated_input_date.strftime("%A")
    number_of_office = len(nearby_dmv_offices_data)
    msg_to_user = f"The date you have on hand is on {formated_input_date} {old_day}!\n I found {number_of_office} location(s) with earlier time than what you have!\n\n"

    response = msg_to_user + "\n".join([f"-------------\n{office['information']}\n" for office in nearby_dmv_offices_data])
    return response


#GOAL: bot想要拆開

#get input: date & zipcode
user_input_date_zipcode = get_input_date_zipcode()


#get user input and convert into datatime
if isinstance(user_input_date_zipcode,list):

    #format user input date as datetime
    formated_input_date = date_handler.make_datetime_formate(user_input_date_zipcode[1])

    #get all nearby dmv offices
    nearby_dmv_offices_data = dmv_api_handler.get_dmv_office_nearby_data_api(user_input_date_zipcode[2])


    #add attribute - 1. earliest_available_date in each nearby_dmv_offices_data & 2. information with find_earlier_date_than_user_input information
    for office in nearby_dmv_offices_data:
        earliest_date= dmv_api_handler.get_date_data_api(office['meta']["dmv_field_office_public_id"])
        office["earliest_available_date"] = date_handler.make_datetime_formate(earliest_date)
        information = date_handler.find_earlier_date_than_user_input(formated_input_date,office["earliest_available_date"],office)
        office["information"] = information


    #NOTIFICATION!
    #METHOD 1.send an email with all avilable ealier time with locations information
    email_handler.send_email(formated_input_date,nearby_dmv_offices_data)

    #METHOD 2.send a notification through Discord
    send_notification_through_discord(formated_input_date,nearby_dmv_offices_data)

    #METHOD 3.send a notification through Discord bot
    # Create an instance of the bot
    bot = commands.Bot(command_prefix="", intents=discord.Intents.all())

    #不需要透過command name 當Event發生時可以直接執行
    # Bot says hi
    @bot.event
    async def on_ready():
        print(f"Hello Penny! Bot is ready for you...")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        print(f"確認 message.content {message.content}")
        date_keyword = ["date", "earlier"]
        distance_keyword = ["miles"]

        message_text = message.content.lower().split()
        print(f"所有的office nearby_dmv_offices_data {nearby_dmv_offices_data}")
        print(f"這邊是一掉所有的空白message_text {message_text}")
        find_or_not = False
        for word in message_text: #['9', 'miles']

            if word in distance_keyword:
                print(f"distance_keyword {distance_keyword}")
                #find the distance the user is looking for
                find_or_not = True
                mile_index = message_text.index(word)
                number_index = mile_index - 1
                print(mile_index, type(mile_index), number_index, type(number_index))
                input_miles = message_text[number_index]
                offices_within_miles = []
                for office in nearby_dmv_offices_data:
                    print(type(office["distance"]), type(input_miles))
                    print(office["distance"], input_miles)

                    if office["distance"] <= float(input_miles):
                        print(f"落入input user要得距離內")
                        offices_within_miles.append(office)
                    else:
                        await message.channel.send(f"I can't find any office within {input_miles} miles")
                        break



                response = format_response(formated_input_date, offices_within_miles)

                await message.channel.send(response)


        if find_or_not is False:
            for word in message_text:
                if word in date_keyword:
                    print(f"date_keyword {date_keyword}")

                    response = format_response(formated_input_date, nearby_dmv_offices_data)

                    await message.channel.send(response)




        # for word in message_text:
        #     if word in date_keyword:
        #         print(f"date_keyword {date_keyword}")

        #         response = format_response(formated_input_date, nearby_dmv_offices_data)

        #         await message.channel.send(response)
        #         break

        #     elif word in distance_keyword:
        #         print(f"distance_keyword {distance_keyword}")
        #         #find the distance the user is looking for
        #         mile_index = message_text.index(word)
        #         number_index = mile_index - 1
        #         print(mile_index, type(mile_index), number_index, type(number_index))
        #         input_miles = message_text[number_index]
        #         offices_within_miles = []
        #         for office in nearby_dmv_offices_data:
        #             print(type(office["distance"]), type(input_miles))
        #             print(office["distance"], input_miles)

        #             if office["distance"] <= float(input_miles):
        #                 print(f"落入input user要得距離內")
        #                 offices_within_miles.append(office)

        #                 response = format_response(formated_input_date, offices_within_miles)

        #                 await message.channel.send(response)

        #         await message.channel.send(f"I can't find any office within {input_miles} miles.")


    bot.run(TOKEN)

else:
    print(user_input_date_zipcode)
