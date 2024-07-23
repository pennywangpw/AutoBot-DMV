from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import string, datetime, asyncio
from String_Handler import StringHandler
from Database_Handler import DatabaseHandler
from Validation_Handler import ValidationHandler
from Date_Handler import DateHandler
import asyncpg
import psycopg2
import psycopg2.extras
from asyncpg.pool import create_pool



# get token
load_dotenv()
TOKEN: Final[str] = os.getenv('TOKEN')


# set up bot
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


#set a response to track if there's record or not
response = {"response":None, "record":None}
print("一起動時的response: ", response)


# create string_handler and database_handler instance
string_handler = StringHandler()
database_handler= DatabaseHandler()
date_handler = DateHandler()
validation_handler= ValidationHandler()


#message functionality- get the response and send to channel
async def send_message(message: Message, res_obj) -> None:
    print("*****send_message---res_obj obj: ", message, res_obj)
    channel = client.get_channel(1186427997851488266)

    is_private = False
    if not res_obj:
        print("Message is empty")
        return

#     #private response
#     is_private = user_message[0] == "?"
#     if is_private :
#         user_message = user_message[1:]

    try:

        # await channel.send("you have search record...let me check it for you again...")

        await message.author.send(res_obj["response"]) if is_private else await channel.send(res_obj["response"])
        return "the message has been sent"


    except Exception as e:
        print("something worng when send message to channel....")
        print(e)


 
async def schedule_daily_message():
    global response
    print("一開始run schedule_daily_message時的response: ", response)
    while True:
        #wait for some time
        now = datetime.datetime.now()
        then = now + datetime.timedelta(minutes= 10)
        wait_time = (then-now).total_seconds()
        print("看看now ",now)
        print("看看then ",then)

        await asyncio.sleep(wait_time)

        #check if there's previous record
        #send message
        channel = client.get_channel(1186427997851488266)
        await channel.send("test by specific time")

        #no previous record
        if response["record"] is None:
            print("***clock自動 並確認沒有之前紀錄")
            await send_message(response,"there's no previous record")

        #there's previous record
        elif response["record"] is not None:
            print("***clock自動 並確認 有之前紀錄: ",response["record"])
            input_record_str = ""
            for input_record in response["record"].values():
                #only collect data which is not none
                if input_record != None:
                    input_record_str = input_record_str + " " + input_record
            await send_message(None,input_record_str)


# handle project if is active
@client.event
async def on_ready():
    print(f"{client.user} is now running!")
    print("*****一開啟")
    database_handler.connect_to_db()
    # await schedule_daily_message()


# Handle incoming messages
@client.event
async def on_message(message: Message) -> None:
    username: str = str(message.author)
    user_message: str = message.content
    user_id = message.author.id
    channel: str = str(message.channel)

    res_obj={}


    # CHECK THE USER
    # Check if bot is responding itself
    if message.author == client.user:
        print("--------------END---------------")
        return

    print("傳送 message 不是 client 自己: ", user_id)

    # Check if current user exists in db member, if not db ++
    if not database_handler.find_the_member(user_id):

        # Insert data in table
        user_email = username + '@sp.com'
        database_handler.insert_member(user_id, user_email, username)


    # CHECK THE RECORD
    if database_handler.find_member_record(user_id):

        #find user record from db
        user_record = database_handler.find_member_record(user_id)


        #get user_record_datetime , user_record_zipcode , user_record_mile
        user_record_datetime =user_record[2]
        user_record_zipcode =user_record[3]
        user_record_mile =user_record[4]



        #remove all the punctuation from user_message (user input)
        user_message_rmv_punctuation = string_handler.remove_punctuation(user_message)


        #conver user_message_rmv_punctuation to list 確認user_message是不是同找到資料的格式,是的話複寫
        user_message_rmv_punctuation_list = user_message_rmv_punctuation.split()
        for word in user_message_rmv_punctuation_list:
            if validation_handler.check_convert_into_num(word) and validation_handler.check_length_zipcode_input_validtion(word):
                user_record_zipcode = word
            elif validation_handler.check_datetime_formate_validation(word):
                user_record_datetime = date_handler.make_string_to_datetime_format(word)
            else:
                user_record_mile = word


        #convert updated user_record_datetime, user_record_zipcode, user_record_mile to string 
        user_record_with_userinput = date_handler.make_datetime_to_string_format(user_record_datetime) + " " +str(user_record_zipcode) + " " + str(user_record_mile)

        

        res_obj = get_response(user_record_with_userinput, False)


        #send message to the channel
        bot_response = await send_message(message, res_obj)

        #save new info in db- update db
        if res_obj["record"]:
            database_handler.update_member_record(user_id,res_obj["record"])


    else:


        #remove all the punctuation to get response
        user_message_rmv_punctuation = string_handler.remove_punctuation(user_message)


        res_obj = get_response(user_message_rmv_punctuation)
  
        #send message to the channel talk to the user
        bot_response = await send_message(message, res_obj)


        #save data in db
        if res_obj["record"]:
            database_handler.insert_record(user_id,res_obj["record"][1],res_obj["record"][0])



# run bot
def main()->None:

    client.run(token=TOKEN)


if __name__ == "__main__":
    main()



