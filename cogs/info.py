from discord.ext import commands

from database.supabase import Supabase

db = Supabase()

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx, channel_id: int = None):
        if channel_id:
            if db.check(channel_id):
                data = db.select_role(channel_id)
                if data[0]["role_id"] != None:
                    await ctx.send(f"{ctx.author.mention}, channel (ID: {channel_id}) is registered with role (ID: {data[0]['role_id']}).")
                else:
                    await ctx.send(f"{ctx.author.mention}, channel (ID: {channel_id}) is registered without a role.")
            else:
                await ctx.send(f"{ctx.author.mention}, channel (ID: {channel_id}) is not registered.")
        else:
            await ctx.send(f"{ctx.author.mention}, you need to specify a channel ID.")
        
    @info.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f"{ctx.author.mention}, argument needs to be of type int.")

async def setup(client: commands.Bot):
    await client.add_cog(Info(client))
