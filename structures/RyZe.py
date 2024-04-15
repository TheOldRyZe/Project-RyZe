import discord
from discord.ext import commands
import os

from structures import utils

import settings.credentials as credentials

from database.database import database_instance


cache_flags = member_cache = discord.MemberCacheFlags(voice=True, joined=False)


class RyZe(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            intents=discord.Intents.all(),
            case_insensitive=True,
            strip_after_prefix=True,
            max_messages=100,
            allowed_mentions=discord.AllowedMentions(users=True),
            cache_flags=cache_flags,
            chunk_guilds_at_startup=False,
            proxy_url=credentials.proxies,
        )


async def get_prefix(client, message):
    prefix_find = prefix_collection.find_one({"id": str(message.guild.id)})
    if prefix_find is None:
        prefix_collection.insert_one(
            {"id": str(message.guild.id), "prefix": credentials.prefix}
        )
    noprefix_find = noprefix_collection.find_one({"id": str(message.author.id)})
    if noprefix_find:
        prefix = commands.when_mentioned_or(prefix_find["prefix"], "")(client, message)
    else:
        prefix = commands.when_mentioned_or(prefix_find["prefix"])(client, message)
    return prefix


client = RyZe()
client.utils = utils
cluster = database_instance()
database = cluster["RyZe"]

prefix_collection = database["prefixes"]
noprefix_collection = database["no_prefixes"]


@client.event
async def on_shard_ready(shard_id):
    guild_count = len(client.guilds)
    print(f"Shard {shard_id} is ready and handling {guild_count} servers.")


@client.event
async def on_ready():
    await client.load_extension("jishaku")
    client.owner_ids = credentials.owners
    print(f"Connected as {client.user}")
    if cluster:
        print("Mongo Initialized")


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    if await utils.is_blacklisted(
        str(message.author.id), "user"
    ) or await utils.is_blacklisted(str(message.guild.id), "guild"):
        return
    await client.process_commands(message)


async def load(path):
    for root, _, files in os.walk(path):
        for filename in files:
            if filename.endswith('.py'):
                cog_path = os.path.relpath(os.path.join(root, filename)).replace(os.sep, '.')[:-3]
                if cog_path.startswith('cogs.'):
                    cog_path = cog_path[len('cogs.'):]
                await client.load_extension(f"cogs.{cog_path}")



async def main():
    async with client:
        await load("./cogs")
        await client.start(credentials.token)
