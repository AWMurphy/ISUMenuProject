# all the fucking imports
from typing import Final
import os
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message
import OldWork.databasingattempt1 as databasingattempt1
from OldWork.responses import get_response
from discord.utils import get
from discord.ext import commands

# time testing
import time
from datetime import datetime
import asyncio

target_hour = 23
target_minute = 11

now = datetime.now()
print(now)

# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
client = Client = Client(intents=intents)

# STEP 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enables probably)')
        return
    if is_private := user_message[0] == '!':
        user_message = user_message[1:]
    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# STEP 3: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    await wait_for_time()

# STEP 4: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# TIME MESSAGE TESTING
async def wait_for_time():
    while True:
        now = datetime.now()
        
        # If current time is 10:40 AM
        if now.hour == target_hour and now.minute == target_minute:
            # print in the general channel 
            channel = client.get_channel(1291094574617595928)
            if channel:
                await channel.send("Hello World! It's time for menus!")
            # adding so I can private message people without chatting
            guild_id = 1291094573950566444  # server's ID: 1291094573950566444
            role_name = "Friley"  # test for just friley because that's what we have

            # get server people + get roles of the type
            guild = client.get_guild(guild_id)
            role = get(guild.roles, name=role_name)
            print(guild)
            print(role)
            if role:
                # Iterate over all members with the role
                for member in guild.members:
                    print(member)
                    if role in member.roles:
                        print(role)
                        try:
                            # Send a private message (DM) to the member WITH ONE FOOD ITEM LISTED
                            list = databasingattempt1.dataBasing()
                            await member.send(f"Hello {member.display_name}, the food at Friley today is: " + (str)(list[0]))
                            print(f"Sent message to {member.display_name}")
                        except Exception as e:
                            print(f"Could not send message to {member.display_name}: {e}")
            else:
                print(f"Role '{role_name}' not found.")
            break
        
        # Wait for 30 seconds before checking the time again
        await asyncio.sleep(10)

# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
