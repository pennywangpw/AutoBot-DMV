from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# get token
load_dotenv()
TOKEN: Final[str] = os.getenv('TOKEN')
print(TOKEN)


# set up bot
# intents: Intents =Intents.default()
# intents.message_content = True
# client: Client = Client(intents=intents)


intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

#message functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Message is empty")
        return
    #private response
    is_private = user_message[0] == "?"
    if is_private :
        user_message = user_message[1:]
    try:
        response: str = get_response(user_message)
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
    await send_message(message,user_message)



def main()->None:
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()
