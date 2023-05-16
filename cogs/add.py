from discord.ext import commands

from database.supabase import Supabase

db = Supabase()

class Add(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command = True)
    @commands.is_owner()
    async def add(self, ctx, channel_id: int = None, role_id: int = None):
        if channel_id:  
            if db.check(channel_id):
                await ctx.send(f"{ctx.author.mention}, channel is already in the database.")
            else:
                if channel_id and role_id:
                    channel = self.client.get_channel(channel_id)
                    if channel:
                        data = db.add(channel_id, role_id)
                        if data == []:
                            await ctx.send(f"{ctx.author.mention}, something went wrong.")
                        else:
                            await ctx.send(f"{ctx.author.mention}, successfully add new channel and role.")
                    else:
                        await ctx.send(f"{ctx.author.mention}, could not find channel (ID: {channel_id}).")
                else:
                    data = db.add(channel_id)
                    if data[0]["channel_id"] == channel_id:
                        await ctx.send(f"{ctx.author.mention}, successfully add new channel.")
                    else:
                        await ctx.send(f"{ctx.author.mention}, something went wrong.")
        else:
            await ctx.send(f"{ctx.author.mention}, you need to specify a channel ID.")

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f"{ctx.author.mention}, every argument needs to be of type int.")
    
    @add.command()
    @commands.is_owner()
    async def role(self, ctx, channel_id: int = None, role_id: int = None):
        if not channel_id:
            await ctx.send(f"{ctx.author.mention}, you need to specify a channel ID.")
        elif channel_id and not role_id:
            await ctx.send(f"{ctx.author.mention}, you need to specify a role ID.")
        else:
            if not db.check(channel_id):
                await ctx.send(f"{ctx.author.mention}, guild is not in the database.")
            else:
                data = db.add_role(channel_id, role_id)
                if data[0]["role_id"] == role_id:
                    await ctx.send(f"{ctx.author.mention}, successfully added role ID for channel: {channel_id}.")
                else:
                    await ctx.send(f"{ctx.author.mention}, something went wrong.")

    @role.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f"{ctx.author.mention}, every argument needs to be of type int.")

async def setup(client: commands.Bot):
    await client.add_cog(Add(client))
