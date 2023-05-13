import time
import datetime

from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["uptime"])
    async def ping(self, ctx):
        uptime = int(time.time() - self.client.start_time)
        await ctx.send(f"⏱️ cozE bot uptime: {str(datetime.timedelta(seconds = uptime))}")

async def setup(client: commands.Bot):
    await client.add_cog(Ping(client))
