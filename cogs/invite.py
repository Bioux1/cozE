import discord

from discord.ext import commands

from config.load_config import init

config = init()

class Invite(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invite(self, ctx):
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label = "Add the bot", style = discord.ButtonStyle.link, url = config["INVITE_LINK"]))
        await ctx.send(f"{ctx.author.mention}, you can add the bot to you server using the link below.", view = view)

async def setup(client: commands.Bot):
    await client.add_cog(Invite(client))
