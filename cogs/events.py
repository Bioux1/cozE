from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged as {self.client.user} (ID: {self.client.user.id})")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            pass

async def setup(client: commands.Bot):
    await client.add_cog(Events(client))
