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



#get user input- either a reminder string or input list
def get_input_date_zipcode():
    if len(sys.argv) == 3:
        input_date = sys.argv[1]
        input_zipcode = int(sys.argv[2])
        validatetion_result = validation_handler.date_zipcode_input_validation(input_date,input_zipcode)
        if validatetion_result is not None:
            return validatetion_result
        else:
            return sys.argv
    else:
        return "Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087)"

#format response
def format_response(formated_input_date, nearby_dmv_offices_data):
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
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send("How may I help you today?")

    @bot.event
    async def on_message(message):
        # check if bot is not responding itself
        if message.author == bot.user:
            return

        #list of keywords
        date_keyword = ["date", "earlier", "dates"]
        distance_keyword = ["miles"]

        #lower and split user input sentense in a list
        message_content_remove_punctuation= remove_punctuation(message.content)
        message_text = message_content_remove_punctuation.lower().split()

        print(f"這邊是一掉所有的空白message_text {message_text}")
        find_or_not = False

        #iterate through each word from user input
        for word in message_text: #['9', 'miles']
            #check if the word is in the keywords list, check if there's a keyword: Miles
            if word.lower() in distance_keyword:
                print(f"user的關鍵字在distance_keyword中 {word}")
                find_or_not = True
                #find the distance the user is looking for
                mile_index = message_text.index(word)
                number_index = mile_index - 1
                input_miles = message_text[number_index]

                #collect offices which are within the miles request
                offices_within_miles = []
                for office in nearby_dmv_offices_data:
                    if office["distance"] <= float(input_miles):
                        offices_within_miles.append(office)

                if not offices_within_miles:
                    await message.channel.send(f"I can't find any office within {input_miles} miles")
                else:
                    response = format_response(formated_input_date, offices_within_miles)
                    await message.channel.send(response)

        #if keyword Miles can't be found, check if there's keyword relates to Date
        if find_or_not is False:
            #iterate through each word from user input
            for word in message_text:
                if word.lower() in date_keyword:
                    response = format_response(formated_input_date, nearby_dmv_offices_data)

                    await message.channel.send(response)
                    find_or_not = True
                    break
            if find_or_not is False:
                await message.channel.send("you may ask me about: find earlier date, find earlier date within specific miles")


    bot.run(TOKEN)

else:
    print(user_input_date_zipcode)
