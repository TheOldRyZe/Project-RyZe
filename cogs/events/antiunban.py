import discord
from discord.ext import commands

import settings.config as config

from structures.utils import *
from structures.checks import antinuke_event_check

from database.database import *


class AntiUnban(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = config.color

    @commands.Cog.listener()
    async def on_ready(self):
        print("Antinuke : Event AntiUnban is Ready")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user) -> None:
        await self.client.wait_until_ready()
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
            if not entry:
                return
            executor = entry.user
            created_timestamp = entry.created_at.timestamp()
            difference = discord.utils.utcnow().timestamp() - created_timestamp
            if difference > 3600:
                return
            check = await antinuke_event_check(executor, guild, "Ban", self.client)
            if check=="Antinuke_Disabled":
                return
            elif check=="Is_Guild_Owner":
                return
            elif check=="Not_Whitelisted":
                await ban(guild.id, executor.id, reason="Member Unban | Not Whitelisted")
                try:
                    await ban(guild.id, user.id, reason="RyZe Recovery | Anti Unban")
                except discord.Forbidden:
                    return


async def setup(client):
    await client.add_cog(AntiUnban(client))