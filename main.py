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

#remember user input
previous_user_input = ""
print("準備前的",previous_user_input)

#remove punctuation marks
def remove_punctuation(user_input_string):
    translator = str.maketrans('', '', string.punctuation)
    result = user_input_string.translate(translator)
    return result

# message functionality
async def send_message(message: Message, user_message: str) -> None:
    global previous_user_input
    if not user_message:
        print("Message is empty")
        return
    #private response
    is_private = user_message[0] == "?"
    if is_private :
        user_message = user_message[1:]
    try:
        user_message_rmv_punctuation= remove_punctuation(user_message)

        # response: str = get_response(user_message_rmv_punctuation)
        response: object = get_response(user_message_rmv_punctuation)

        print("準備紀錄zipcode and date",response)
        # await message.author.send(response) if is_private else await message.channel.send(response)
        await message.author.send(response["response"]) if is_private else await message.channel.send(response["response"])

        #check if there's previous user input
        if response["record"]["zipcode"]:
            previous_user_input = previous_user_input + " " +  response["record"]["zipcode"]
        if response["record"]["datetime"]:
            previous_user_input = previous_user_input + " " + response["record"]["datetime"]
        if response["record"]["mile_range"]:
            previous_user_input = previous_user_input + " " + response["record"]["mile_range"]

        print("準備後的",previous_user_input)

    except Exception as e:
        print("有錯誤")
        print(e)



async def schedule_daily_message():
    while True:
        #wait for some time
        now = datetime.datetime.now()
        then = now + datetime.timedelta(minutes= 1)
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
