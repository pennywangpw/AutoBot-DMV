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


#interactive bot
TOKEN = 'MTE4NjQyNDc1MDcyNjIwNTQ1MQ.G0Y9jN.3Xoh8NisJRCr1HSImHXj5WALar22MUApA-8W0o'
CHANNEL_ID = 1186427997851488266


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




#GOAL: bot想要拆開

#get input: date & zipcode
user_input_date_zipcode = get_input_date_zipcode()
print(f"檢查 user_input_date_zipcode {user_input_date_zipcode}")

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



    #send an email with all avilable ealier time with locations information
    # send_email(formated_input_date,nearby_dmv_offices_data)
    email_handler.send_email(formated_input_date,nearby_dmv_offices_data)
    send_notification_through_discord(formated_input_date,nearby_dmv_offices_data)

    # Create an instance of the bot
    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
    # Define a command for the bot
    @bot.command(name="update")
    async def update_command(ctx):
        # Respond to the Discord user with the data
        old_day = formated_input_date.strftime("%A")
        number_of_office = len(nearby_dmv_offices_data)
        msg_to_user = f"The date you have on hand is on {formated_input_date} {old_day}!\n I found {number_of_office} location(s) with earlier time than what you have!\n\n"

        response = msg_to_user + "\n".join([f"-------------\n{office['information']}\n" for office in nearby_dmv_offices_data])
        await ctx.send(response)
    bot.run(TOKEN)

else:
    print(user_input_date_zipcode)
