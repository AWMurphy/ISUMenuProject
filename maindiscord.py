from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# time testing
import time
from datetime import datetime
import asyncio

target_hour = 10
target_minute = 44

now = datetime.now()
print(now)

# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
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
@client.event
async def wait_for_time():
    while True:
        now = datetime.now()
        
        # If current time is 10:40 AM
        if now.hour == target_hour and now.minute == target_minute:
            # Get the channel you want the bot to send a message to (replace 'CHANNEL_ID' with your actual channel ID)
            channel = client.get_channel(1291094574617595928)
            if channel:
                await channel.send("Hello World")
            break
        
        # Wait for 30 seconds before checking the time again
        await asyncio.sleep(30)

# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
