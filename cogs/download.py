import os
import discord
import asyncpraw

from discord.ext import commands
from redvid import Downloader

from config.load_config import init

config = init()

class Download(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit = asyncpraw.Reddit(client_id = config["REDDIT_CLIENT"], client_secret = config["REDDIT_SECRET"], user_agent = config["REDDIT_USER"])
        self.downloader = Downloader(max_q = True)

    @commands.command(aliases = ["dl", "save", "fetch"])
    async def download(self, ctx, post = None):
        if post:
            try:
                submission = await self.reddit.submission(url = post)
            except Exception as e:
                await ctx.send(f"{ctx.author.mention}, Error getting the Reddit post: " + str(e))
                return
            if submission.is_video:
                self.downloader.url = submission.url
                file = self.downloader.download()
                await ctx.send(f"{ctx.author.mention}, here is the video:", file = discord.File(file))
                os.remove(file)
            elif submission.is_reddit_media_domain:
                await ctx.send(f"{ctx.author.mention}, {submission.url}")
            else:
                await ctx.send(f"{ctx.author.mention}, post does not contain any media.")
        else:
            await ctx.send(f"{ctx.author.mention}, you need to specify a post url.")

async def setup(client: commands.Bot):
    await client.add_cog(Download(client))
