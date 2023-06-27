from discord.ext import commands

from database.supabase import Supabase

db = Supabase()

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx):
        if not db.check_guild(ctx.guild.id):
            await ctx.send(f"{ctx.author.mention}, There is no existing configuration for this server. Run `$setup` to set up a configuration.")
        else:
            data = db.select_guild(ctx.guild.id)
            message = f"{ctx.author.mention}, current configuration for server (ID: {ctx.guild.id}): \nChannel: <#{data[0]['channel_id']}> \n"
            user = self.client.get_user(data[0]["role_id"])
            if user:
                message += f"User: <@{data[0]['role_id']}>"
                await ctx.send(message)
            else:
                message += f"Role: <@&{data[0]['role_id']}>"
                await ctx.send(message)

async def setup(client: commands.Bot):
    await client.add_cog(Info(client))
