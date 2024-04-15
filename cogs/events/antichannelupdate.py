import discord
from discord.ext import commands

import settings.config as config

from structures.utils import *
from structures.checks import antinuke_event_check

from database.database import *


class AntiChannelUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = config.color

    @commands.Cog.listener()
    async def on_ready(self):
        print("Antinuke : Event AntiChannelUpdate is Ready")


    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after) -> None:
        await self.client.wait_until_ready()
        guild = before.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(limit=2, action=discord.AuditLogAction.channel_update):
            if not entry:
                return
            executor = entry.user
            created_timestamp = entry.created_at.timestamp()
            difference = discord.utils.utcnow().timestamp() - created_timestamp
            if difference > 3600:
                return
            check = await antinuke_event_check(executor, guild, "Channel_Update", self.client)
            if check=="Antinuke_Disabled":
                return
            elif check=="Is_Guild_Owner":
                return
            elif check=="Not_Whitelisted":
                try:
                    await ban(guild.id, executor.id, reason="Channel Update | Not Whitelisted")
                    if isinstance(after, discord.TextChannel):
                        return await after.edit(name=before.name, topic=before.topic, rate_limit_per_user=before.slowmode_delay, nsfw=before.nsfw)
                    elif isinstance(after, discord.CategoryChannel):
                        return await after.edit(name=before.name)
                    elif isinstance(after, discord.VoiceChannel):
                        return await after.edit(name=before.name, rtc_region=before.rtc_region, video_quality_mode=before.video_quality_mode,
                                    user_limit=before.user_limit, bitrate=before.bitrate, rate_limit_per_user=before.slowmode_delay,
                                    nsfw=before.nsfw)
                    else:
                        return
                except discord.Forbidden:
                    return
                


    
async def setup(client):
    await client.add_cog(AntiChannelUpdate(client))