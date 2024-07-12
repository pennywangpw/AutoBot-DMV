from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import string, datetime, asyncio
from String_Handler import StringHandler
from Database_Handler import DatabaseHandler
from Validation_Handler import ValidationHandler
import asyncpg
import psycopg2
import psycopg2.extras
from asyncpg.pool import create_pool


validation_handler= ValidationHandler()

# get token
load_dotenv()
TOKEN: Final[str] = os.getenv('TOKEN')
print("main裡面的token: ",TOKEN)


# set up bot
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


# #set up db- credentials
# hostname ="127.0.0.1"
# database = "dmv_bot"
# username = "postgres"
# pwd = "postgres"
# port_id = 5432
# conn = None
# cur = None


#set a response to track if there's record or not
response = {"response":None, "record":None}
print("一起動時的response: ", response)


# create string_handler and database_handler instance
string_handler = StringHandler()
database_handler= DatabaseHandler()

#remove punctuation marks
def remove_punctuation(user_input_string):
    translator = str.maketrans('', '', string.punctuation)
    result = user_input_string.translate(translator)
    return result

#message functionality- get the response and send to channel
async def send_message(message: Message, user_message) -> None:
    print("*****send_message---user_message 應該都要是string: ", message, user_message)

    global response
    is_private = False
    if not user_message:
        print("Message is empty")
        return

    #private response
    is_private = user_message[0] == "?"
    if is_private :
        user_message = user_message[1:]

    try:
        #remove all the punctuation and run user input checker
        user_message_rmv_punctuation = string_handler.remove_punctuation(user_message)
        print("拿掉標點符號的樣子ˋ,",user_message_rmv_punctuation)

        response = get_response(message,user_message_rmv_punctuation)


        print("準備紀錄zipcode and date",response)
        channel = client.get_channel(1186427997851488266)
        # await message.author.send(response) if is_private else await message.channel.send(response)
        # await message.author.send(response["response"]) if is_private else await message.channel.send(response["response"])
        await message.author.send(response["response"]) if is_private else await channel.send(response["response"])
        return response


    except Exception as e:
        print("有錯誤")
        print(e)



async def schedule_daily_message():
    global response
    print("一開始run schedule_daily_message時的response: ", response)
    while True:
        #wait for some time
        now = datetime.datetime.now()
        then = now + datetime.timedelta(minutes= 1)
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
    await schedule_daily_message()

#insert data
async def insert_user_data(email, username):
    print("-----here's insert data function----", email , username)
    conn = None
    try:
        conn = await asyncpg.connect(
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            host=HOST
        )

        sql = '''INSERT INTO "members" (email, username) VALUES ($1, $2)'''
        sql2 = '''INSERT INTO "records" (zipcode, datetime) VALUES ($1, $2)'''

        await conn.execute(sql, email, username)
        await conn.execute(sql2, 95035, '20240420')

        print("Data has been inserted successfully!")

    except Exception as e:
        print("Error occurred while inserting data:", e)

    finally:
        if conn:
            await conn.close()

# handle incoming messages
@client.event
async def on_message(message: Message)-> None:

    username: str = str(message.author)
    user_message: str = message.content
    user_id = message.author.id
    channel: str = str(message.channel)

    global response
    print("*****當user有輸入任何文字時")
    print("on_message on fire時候的response: ", response)
    # check if bot is responding itself
    if message.author == client.user:
        print("傳送message的是client自己")
        print("--------------END---------------")
        return

    print("傳送message 不是client自己: ", user_id)
    #check if current user exists in db member
    if database_handler.find_the_member(user_id):
        print("current user exists in db member")
    else:
        #insert data in table
        user_email = username + '@sporton.com'
        print("存入user_id,user_email,username： ",user_id,user_email,username, type(user_id))
        database_handler.insert_member(user_id,user_email,username)

    print(f"[{channel}] {username}: '{user_message}'")
    print("這裡的message: ", message)

    #check if there's no record in response
    if database_handler.find_member_record(user_id):
        print("find the member record!!")
    else:
        print("i'm going to insert member record" )
        bot_response = await send_message(message,user_message)
        #insert record
        test = ["20240615","95035"]
        test_datetime, test_zipcode =  validation_handler.check_zipcode_datetime_provided_and_valid(test)
        database_handler.insert_record(user_id ,test_datetime, test_zipcode)

        print("in main what response i got: ", bot_response)





# run bot
def main()->None:

    client.run(token=TOKEN)


if __name__ == "__main__":
    main()
