import discord
from responses import handle_response
import json


async def send_message(message, user_message, is_private):
    try:
        color, title, response = handle_response(message, user_message, is_private)
        await message.author.send(
            embed=discord.Embed(color=color, title=title, description=response)
        ) if is_private else await message.channel.send(
            embed=discord.Embed(color=color, title=title, description=response)
        )
    # TODO Exceptions
    except Exception as e:
        print(e)


def run_bot():
    # Read a token from config.json
    f = open("config.json")
    data = json.load(f)
    f.close()
    TOKEN = data["token"]
    # Bot configuration
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print("{} is now running!".format(client.user))

    @client.event
    # Run this when someone sends a message
    async def on_message(message):
        if message.author != client.user:
            # username = str(message.author)
            usr_message = str(message.content)
            # channel = str(message.channel)
            if usr_message[0] == "-":
                if usr_message[1] == "-":
                    # Remove first two characters, '--' means private message
                    usr_message = usr_message[2:]
                    await send_message(message, usr_message, is_private=True)
                else:
                    # Remove first character of message string if it is '-'
                    usr_message = usr_message[1:]
                    await send_message(message, usr_message, is_private=False)

    # Run the bot
    client.run(TOKEN)
