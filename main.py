from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import string, datetime, asyncio

# get token
load_dotenv()
TOKEN: Final[str] = os.getenv('TOKEN')
print("main裡面的token: ",TOKEN)


# set up bot
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

#set a response to track if there's record or not
response = {"response":None, "record":None}
print("一起動時的response: ", response)

#remove punctuation marks
def remove_punctuation(user_input_string):
    translator = str.maketrans('', '', string.punctuation)
    result = user_input_string.translate(translator)
    return result

#message functionality
async def send_message(message: Message, user_message: str) -> None:
    global response
    if not user_message:
        print("Message is empty")
        return

    #private response
    is_private = user_message[0] == "?"
    if is_private :
        user_message = user_message[1:]

    #check if there's no response record
    print("檢查是否有record---",response["record"])
    if response["record"] is None:
        print("進到這裡代表之前迷u有紀錄")

        try:
            user_message_rmv_punctuation= remove_punctuation(user_message)

            # response: object = get_response(user_message_rmv_punctuation)
            response = get_response(user_message_rmv_punctuation)


            print("準備紀錄zipcode and date",response)
            # await message.author.send(response) if is_private else await message.channel.send(response)
            await message.author.send(response["response"]) if is_private else await message.channel.send(response["response"])

        except Exception as e:
            print("有錯誤-沒有之前的紀錄")
            print(e)

    #check if there's response record
    elif response["record"] is not None:
        print("之前有紀錄的")

        try:
            #pull out previous record
            previous_user_input = response["record"].values()
            previous_user_input_str = ""
            for val in previous_user_input:
                if val != None:
                    previous_user_input_str = previous_user_input_str + " " +  val

            #add current user input
            previous_user_input_str = previous_user_input_str + " " +  user_message


            if previous_user_input_str != "":
                response = get_response(previous_user_input_str)

            await message.author.send(response["response"]) if is_private else await message.channel.send(response["response"])


            print("準備後的",previous_user_input)
            print("準備後的previous_user_input_str",previous_user_input_str)

        except Exception as e:
            print("有錯誤-有之前的紀錄")
            print(e)

    print("====send message後的 response: ",response)

async def schedule_daily_message():
    while True:
        #wait for some time
        now = datetime.datetime.now()
        then = now + datetime.timedelta(minutes= 10)
        wait_time = (then-now).total_seconds()
        print("看看now ",now)
        print("看看then ",then)

        await asyncio.sleep(wait_time)

        #send message
        channel = client.get_channel(1186427997851488266)
        await channel.send("test by specific time")

# handle incoming messages
@client.event
async def on_ready():
    print(f"{client.user} is now running!")
    await schedule_daily_message()

@client.event
async def on_message(message: Message)-> None:
    # check if bot is not responding itself
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f"[{channel}] {username}: '{user_message}'")
    print("這裡的message: ", message)
    await send_message(message,user_message)



# run bot
def main()->None:
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()
