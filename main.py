from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import string

# get token
load_dotenv()
TOKEN: Final[str] = os.getenv('TOKEN')
print("main裡面的token: ",TOKEN)


# set up bot
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

#remove punctuation marks
def remove_punctuation(user_input_string):
    translator = str.maketrans('', '', string.punctuation)
    result = user_input_string.translate(translator)
    return result

# message functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Message is empty")
        return
    #private response
    is_private = user_message[0] == "?"
    if is_private :
        user_message = user_message[1:]
    try:
        user_message_rmv_punctuation= remove_punctuation(user_message)

        response: str = get_response(user_message_rmv_punctuation)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print("有錯誤")
        print(e)


# handle incoming messages
@client.event
async def on_ready():
    print(f"{client.user} is now running!")


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
