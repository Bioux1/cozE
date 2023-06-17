import os
import discord
import asyncpraw
import requests
import json

from discord.ext import commands
from redvid import Downloader

from config.load_config import init

config = init()

class Download(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit = asyncpraw.Reddit(client_id = config["REDDIT_CLIENT"], client_secret = config["REDDIT_SECRET"], user_agent = config["REDDIT_USER"])
        self.downloader = Downloader(max_q = True)
        self.downloader.log = False
        self.url = "https://kappa.lol/api/upload"

    @commands.command(aliases = ["dl", "save", "fetch"])
    async def download(self, ctx, post = None):
        if post:
            try:
                submission = await self.reddit.submission(url = post)
                progress = await ctx.send("Downloading...")
            except Exception as e:
                await ctx.send(f"{ctx.author.mention}, error getting the Reddit post: " + str(e))
                return
            if submission.is_video:
                self.downloader.url = submission.url
                file_temp = self.downloader.download()
                file_size = os.path.getsize(file_temp)
                if file_size > ctx.guild.filesize_limit:
                    await progress.edit(content = "File is larger than the server size limit, uploading to kappa.lol...")
                    file = {"file": open(file_temp, "rb")}
                    response = requests.post(self.url, files = file)
                    response_data = json.loads(response.text)
                    await progress.edit(content = f"{ctx.author.mention}, here is the video: \n{response_data['link']}")
                    file["file"].close()
                else:
                    await progress.edit(content = f"{ctx.author.mention}, here is the video:", attachments = [discord.File(file_temp)])
                os.remove(file_temp)
            elif submission.is_reddit_media_domain:
                await progress.edit(content = f"{ctx.author.mention}, {submission.url}")
            else:
                await progress.edit(content = f"{ctx.author.mention}, post does not contain any media.")
        else:
            await ctx.send(f"{ctx.author.mention}, you need to specify a post url.")

async def setup(client: commands.Bot):
    await client.add_cog(Download(client))