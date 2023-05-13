from discord.ext import commands

class Source(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def source(self, ctx):
        await ctx.send(f"{ctx.author.mention}, https://github.com/Bioux1/cozE")

async def setup(client: commands.Bot):
    await client.add_cog(Source(client))
