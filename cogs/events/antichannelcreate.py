import discord
from discord.ext import commands

import settings.config as config

from structures.utils import *
from structures.checks import antinuke_event_check

from database.database import *


class AntiChannelCreate(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = config.color

    @commands.Cog.listener()
    async def on_ready(self):
        print("Antinuke : Event AntiChannelCreate is Ready")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel) -> None:
        await self.client.wait_until_ready()
        guild = channel.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        try:
            async for entry in guild.audit_logs(limit=2, action=discord.AuditLogAction.channel_create):
                if not entry:
                    return
                executor = entry.user
                created_timestamp = entry.created_at.timestamp()
                difference = discord.utils.utcnow().timestamp() - created_timestamp
                if difference > 3600:
                    return
                check = await antinuke_event_check(executor, guild, "Channel_Create", self.client)
                if check=="Antinuke_Disabled":
                    return
                elif check=="Is_Guild_Owner":
                    return
                elif check=="Not_Whitelisted":
                    await ban(guild.id, executor.id, reason="Channel Create | Not Whitelisted")
                    try:
                        await channel.delete()
                    except discord.HTTPException:
                        await sleep(10)
                    except:
                        return
                break
        except discord.HTTPException:
            await sleep(10)

    
async def setup(client):
    await client.add_cog(AntiChannelCreate(client))