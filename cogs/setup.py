import discord
import asyncio

from discord.ext import commands

from database.supabase import Supabase

db = Supabase()

class Setup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command = True)
    @commands.has_permissions(manage_roles = True, manage_channels = True)
    async def setup(self, ctx):
        def check(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel
        if db.check_guild(ctx.guild.id):
            await ctx.send(f"{ctx.author.mention},You can only add one channel per server! If you want to change the current configuration run `$setup edit`.")
        else:
            await ctx.send(f"{ctx.author.mention}, Welcome to {self.client.user} setup! \
                        \nPlease send the channel where you want the free games to be announced (e.g., `#free-games`), channel ID also works.")
            try:
                channel_message = await self.client.wait_for("message", check = check, timeout = 30.0)
                channel = None
                if channel_message.content.isdigit():
                    channel = self.client.get_channel(int(channel_message.content))
                if not channel:
                    channel = discord.utils.get(ctx.guild.channels, mention = channel_message.content)
                if not channel:
                    channel = discord.utils.get(ctx.guild.channels, name = channel_message.content)
                if not channel:
                    await ctx.send(f"{ctx.author.mention}, Invalid channel provided! Please try again")
                    return
            except asyncio.TimeoutError:
                await ctx.send("Setup command timed out! Please try again.")
            await ctx.send("Now please send the role or user you want to mention when announcing free games (e.g., `@games-notification` or `@forsen`), IDs also works. \
                        \nYou can also send `None` if you don't want to mention a role or a user.")
            try:
                role_message = await self.client.wait_for("message", check = check, timeout = 30.0)
                if role_message.content.lower() == "none":
                    progress = await ctx.send("Saving guild and channel in the database...")
                    data = db.add(ctx.guild.id, channel.id)
                    if data[0]["guild_id"] == ctx.guild.id and data[0]["channel_id"] == channel.id:
                        await progress.edit(content = f"{ctx.author.mention}, Successfully saved configuration for server (ID: {ctx.guild.id})")
                        return
                    else:
                        await progress.edit(content = f"{ctx.author.mention}, something went wrong, please try again.")
                        return
                role = None
                if role_message.content.isdigit():
                    role = ctx.guild.get_role(int(role_message.content))
                    if not role:
                        role = ctx.guild.get_member(int(role_message.content))
                if not role:
                    role = discord.utils.get(ctx.guild.roles, mention = role_message.content)
                if not role:
                    role = discord.utils.get(ctx.guild.roles, name = role_message.content)
                if not role:
                    mentioned_user = role_message.mentions
                    if mentioned_user:
                        role = mentioned_user[0]
                if not role:
                    await ctx.send(f"{ctx.author.mention}, Invalid role or user provided! Please try again.")
                    return
                progress = await ctx.send("Saving configuration in the database...")
                data = db.add(ctx.guild.id, channel.id, role.id)
                if data[0]["guild_id"] == ctx.guild.id and data[0]["channel_id"] == channel.id and data[0]["role_id"] == role.id:
                    await progress.edit(content = f"{ctx.author.mention}, Successfully saved configuration for server (ID: {ctx.guild.id})")
                    return
                else:
                    await progress.edit(content = f"{ctx.author.mention}, something went wrong, please try again.")
                    return
            except asyncio.TimeoutError:
                await ctx.send("Setup command timed out! Please try again.")
    
    @setup.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention}, you need the `Manage Roles` and `Manage Channels` permissions to run this command!")

    @setup.command()
    @commands.has_permissions(manage_roles = True, manage_channels = True)
    async def edit(self, ctx):
        def check(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel
        if not db.check_guild(ctx.guild.id):
            await ctx.send(f"{ctx.author.mention}, There is no existing configuration to edit. Run `$setup` to set up a configuration.")
            return
        await ctx.send(f"{ctx.author.mention}, You are about to edit the configuration for server (ID: {ctx.guild.id}). \
                       \nPlease send the new channel where you want the free games to be announced (e.g., `#free-games`), channel ID also works.")
        try:
            channel_message = await self.client.wait_for("message", check = check, timeout = 30.0)
            channel = None
            if channel_message.content.isdigit():
                channel = self.client.get_channel(int(channel_message.content))
            if not channel:
                channel = discord.utils.get(ctx.guild.channels, mention = channel_message.content)
            if not channel:
                channel = discord.utils.get(ctx.guild.channels, name = channel_message.content)
            if not channel:
                await ctx.send(f"{ctx.author.mention}, Invalid channel provided! Please try again.")
                return
        except asyncio.TimeoutError:
            await ctx.send("Setup command timed out! Please try again.")
        await ctx.send("Now please send the new role or user you want to mention when announcing free games (e.g., `@games-notification` or `@forsen`), IDs also work. \
                       \nYou can also send `None` if you don't want to mention a role or a user.")
        try:
            role_message = await self.client.wait_for("message", check = check, timeout = 30.0)
            if role_message.content.lower() == "none":
                progress = await ctx.send("Updating guild and channel in the database...")
                data = db.update(ctx.guild.id, channel.id)
                if data[0]["guild_id"] == ctx.guild.id and data[0]["channel_id"] == channel.id:
                    await progress.edit(content = f"{ctx.author.mention}, Successfully updated configuration for server (ID: {ctx.guild.id})")
                    return
                else:
                    await progress.edit(content = f"{ctx.author.mention}, Something went wrong, please try again.")
                    return
            role = None
            if role_message.content.isdigit():
                role = ctx.guild.get_role(int(role_message.content))
                if not role:
                    role = ctx.guild.get_member(int(role_message.content))
            if not role:
                role = discord.utils.get(ctx.guild.roles, mention = role_message.content)
            if not role:
                role = discord.utils.get(ctx.guild.roles, name = role_message.content)
            if not role:
                mentioned_user = role_message.mentions
                if mentioned_user:
                    role = mentioned_user[0]
            if not role:
                await ctx.send(f"{ctx.author.mention}, Invalid role or user provided! Please try again.")
                return
            progress = await ctx.send("Updating configuration in the database...")
            data = db.update(ctx.guild.id, channel.id, role.id)
            if data[0]["guild_id"] == ctx.guild.id and data[0]["channel_id"] == channel.id and data[0]["role_id"] == role.id:
                await progress.edit(content = f"{ctx.author.mention}, Successfully updated configuration for server (ID: {ctx.guild.id})")
            else:
                await progress.edit(content = f"{ctx.author.mention}, Something went wrong, please try again.")
                return
        except asyncio.TimeoutError:
            await ctx.send("Setup command timed out! Please try again.")

    @edit.error
    async def edit_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention}, you need the `Manage Roles` and `Manage Channels` permissions to run this command!")

    @setup.command()
    @commands.has_permissions(manage_roles = True, manage_channels = True)
    async def reset(self, ctx):
        progress = await ctx.send(f"{ctx.author.mention}, reseting configation for server (ID: {ctx.guild.id})...")
        data = db.delete(ctx.guild.id)
        if data[0]["guild_id"] == ctx.guild.id:
            await progress.edit(content = f"{ctx.author.mention}, Successfully reinitialized configuration for server (ID: {ctx.guild.id})")

    @reset.error
    async def reset_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention}, you need the `Manage Roles` and `Manage Channels` permissions to run this command!")
        
async def setup(client: commands.Bot):
    await client.add_cog(Setup(client))
