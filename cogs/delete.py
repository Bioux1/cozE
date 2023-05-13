from discord.ext import commands

from database.supabase import Supabase

db = Supabase()

class Delete(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases = ["del"], invoke_without_command=True)
    @commands.is_owner()
    async def delete(self, ctx, channel_id: int = None):
        if channel_id:
            if db.check(channel_id):
                data = db.delete(channel_id)
                if data != []:
                    await ctx.send(f"{ctx.author.mention}, successfully deleted channel and role.")
                else:
                    await ctx.send(f"{ctx.author.mention}, something went wrong.")
            else:
                await ctx.send(f"{ctx.author.mention}, channel is not in the database.")
        else:
            await ctx.send(f"{ctx.author.mention}, you need to specify a channel ID.")

    @delete.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f"{ctx.author.mention}, every argument needs to be of type int.")

    @delete.command()
    @commands.is_owner()
    async def role(self, ctx, channel_id: int = None):
        if channel_id:
            if db.check_role(channel_id):
                data = db.delete_role(channel_id)
                if data[0]["role_id"]:
                    await ctx.send(f"{ctx.author.mention}, something went wrong")
                else:
                    await ctx.send(f"{ctx.author.mention}, successfully deleted role ID for channel: {channel_id}.")
            else:
                await ctx.send(f"{ctx.author.mention}, no role is assigned for this channel.")
        else:
            await ctx.send(f"{ctx.author.mention}, you need to specify a channel ID.")

    @role.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f"{ctx.author.mention}, every argument needs to be of type int.")

async def setup(client: commands.Bot):
    await client.add_cog(Delete(client))
