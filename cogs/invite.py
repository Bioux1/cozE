import discord
import datetime
import pytz

from discord import ui
from discord.ext import commands

from config.load_config import init

config = init()

class request_button(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label = "Add the bot", style = discord.ButtonStyle.link, url = config["INVITE_LINK"]))
    
    @discord.ui.button(label = "request cozE bot", style = discord.ButtonStyle.grey, emoji = "<:cozE:1094387800494837781>")
    async def request(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(request_modal())

class request_modal(discord.ui.Modal, title = "Request cozE bot for your own server"):
    description = ui.TextInput(label = "Description", placeholder = "Short description on why you'd like the bot added to your server, English only!", style = discord.TextStyle.paragraph, required = True)
    channel_id = ui.TextInput(label = "Channel ID", placeholder = "The ID of the channel where you want to receive free games alert", min_length = 18, max_length = 18, style = discord.TextStyle.paragraph, required = True)
    role_id = ui.TextInput(label = "Role ID (optional)  ", placeholder = "Role ID or user ID mentionned when announcing free games", min_length = 18, max_length = 18, style = discord.TextStyle.paragraph, required = False)
    
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title = f"New request from {interaction.user} (ID: {interaction.user.id})", description = self.description)
        embed.colour = discord.Colour.from_rgb(66, 78, 102)
        embed.add_field(name = "Channel ID:", value = self.channel_id)
        embed.add_field(name = "Role ID:", value = self.role_id)
        embed.timestamp = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
        await request_channel.send("<@430001704159936512>", embed = embed)
        await interaction.response.send_message(f"{interaction.user.mention}, request sent successfully.")

class Invite(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["request"])
    async def invite(self, ctx):
        global request_channel
        request_channel = self.client.get_channel(1046838153400569987)
        await ctx.send(f"{ctx.author.mention}, if you want to add cozE bot to your own server please click the button below and fill out the form. Before submitting the form please add the bot to you server using the link below.", view = request_button())

async def setup(client: commands.Bot):
    await client.add_cog(Invite(client))
