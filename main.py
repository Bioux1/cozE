import discord
import time
import asyncio

from discord.ext import commands

from config.load_config import init

activity = discord.Game(name = "$about")
client = commands.Bot(command_prefix = ("$"), activity = activity, intents = discord.Intents(message_content = True, messages = True, guilds = True, members = True))

extensions = (
    "cogs.events",
    "cogs.invite",
    "cogs.ping",
    "cogs.about",
    "cogs.source",
    "cogs.info",
    "cogs.reddit",
    "cogs.download",
    "cogs.setup"
)

async def main():
    async with client:
        for extension in extensions:
            try:
                await client.load_extension(extension)
            except Exception as e:
                print("Failed to load extension: ", e)
        await client.start(config["TOKEN"], reconnect = True)

config = init()
client.start_time = time.time()
client.request_channel = client.get_channel(config["REQUEST_CHANNEL_ID"])

asyncio.run(main())
