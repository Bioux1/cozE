import discord
import pytz
import asyncpraw

from datetime import datetime
from discord.ext import commands
from discord.ext import tasks

from config.load_config import init
from database.supabase import Supabase

db = Supabase()
config = init()

class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.subreddit_name = "GameDeals"
        self.reddit = asyncpraw.Reddit(client_id = config["REDDIT_CLIENT"], client_secret = config["REDDIT_SECRET"], user_agent = config["REDDIT_USER"])
        self.check_posts.start()

    def create_embed(self, post):
        created_time = datetime.fromtimestamp(post.created_utc, tz = pytz.utc)
        formatted_time = created_time.astimezone(pytz.timezone('Europe/Stockholm')).strftime("%B %d, %Y at %I:%M%p")
        embed = discord.Embed(title = post.title, description = post.url)
        embed.colour = 16733952
        embed.set_footer(text=f"via /r/GameDeals | {formatted_time}")
        return embed

    @tasks.loop(minutes = 15)
    async def check_posts(self):
        channels = db.select()
        subreddit = await self.reddit.subreddit(self.subreddit_name)
        new_posts_ids = []
        previous_post_ids = []
        for id in db.select_post_ids():
            previous_post_ids.append(id["id"])
        async for post in subreddit.new():
            new_posts_ids.append(post.id)
            if post.id in previous_post_ids:
                continue
            db.insert_post_id(post.id)
            if "free" in post.title.lower() and "100%" in post.title.lower():
                embed = self.create_embed(post)
                for d in channels:
                    channel = self.client.get_channel(d["channel_id"])
                    if d["role_id"]:
                        user = self.client.get_user(d["role_id"])
                        if user:
                            await channel.send(f"<@{d['role_id']}>", embed = embed)
                        else:
                            await channel.send(f"<@&{d['role_id']}>", embed = embed)
                    else:
                        await channel.send(embed = embed)
        db.remove_old_posts_ids(new_posts_ids)

    @check_posts.before_loop
    async def before_check_post(self):
        await self.client.wait_until_ready()

async def setup(client: commands.Cog):
    await client.add_cog(Reddit(client))
