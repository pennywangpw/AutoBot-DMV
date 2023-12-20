import discord
from discord.ext import commands
from api import get_sj_date_data_api,get_date_data_api,get_time_slot_data_api,get_dmv_office_nearby_data_api
from shared_data import nearby_dmv_offices




TOKEN = 'MTE4NjQyNDc1MDcyNjIwNTQ1MQ.GIf3zY.pFG2ET_bEssLgfX7aKGqRui-vTIfY_DlysylrU'
CHANNEL_ID = 1186427997851488266

# Create an instance of the bot
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("JUST WANT TO KNOW IF THIS IS WORKING-bot ready")

    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! the bot is ready :)")
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

# Define a command to send a notification
@bot.command(name='send_notification')
async def send_notification(ctx, *, message):
    # Replace 'CHANNEL_ID' with the ID of the channel where you want to send the notification
    channel = bot.get_channel(CHANNEL_ID)

    # Send the notification
    await channel.send(message)

@bot.command(name='add')
async def add(ctx, x,y):
    try:
        result = int(x) + int(y)
        await ctx.send(f"{x} + {y} = {result}")
    except Exception as e:
        await ctx.send("add fuction error")


# @bot.command(name='on_message')
@bot.event
async def on_message(message):
    print(f"message content是什麼 {message.content}")
    print(f"是否有帶進來 nearby_dmv_offices {nearby_dmv_offices}")
    if message.author == bot.user:
        return
    if message.content == "update":
        await message.channel.send("available dates: ")
        for office in nearby_dmv_offices:
            print(f"test office {office}")
            await message.channel.send(office['information'])
# Process commands
    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)
