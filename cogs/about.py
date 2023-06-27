from discord.ext import commands

class About(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def about(self, ctx):
        await ctx.send(f"{ctx.author.mention}, <a:YEAHBUTBTTV:1095059686933418215> 💢 WHAT IS THIS BOT ABOUT ?! \
                       \nThis bot sends a notifications message every time a game is free for a limited time on various stores, based on the r/GameDeals subreddit. Open Source and written in Python. \
                       \n<https://clips.twitch.tv/ExpensiveWonderfulClamArsonNoSexy> <:4HEad:1095059962000052364> \nStart using the bot by running the `$setup` command!")

async def setup(client: commands.Bot):
    await client.add_cog(About(client))
