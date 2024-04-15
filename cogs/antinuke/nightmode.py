import discord
from discord.ext import commands

from structures.utils import *
from structures.checks import *

import settings.config as config
import settings.links as links


from database.database import *
collection = "rand"


class Nightmode(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = config.color

    @commands.Cog.listener()
    async def on_ready(self):
        print("Antinuke : NightMode Ready")

    @commands.group(invoke_without_command=True)
    async def nightmode(self, ctx):
        embed = discord.Embed(
            title="Nightmode Command Help",
            description="Use these commands to manage Nightmode settings:",
            color=self.color,
        )
        embed.add_field(
            name="nightmode enable", value="Enable's NightMode For The Server", inline=False
        )
        embed.add_field(
            name="nightmode disable", value="Disable's NightMode For The Server", inline=False
        )
        embed.set_footer(
            text="Requested by {}".format(ctx.author.display_name),
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=embed)


    @nightmode.command(aliases=["on"])
    @nightmode_check()
    async def enable(self, ctx):
        await ctx.send(embed=discord.Embed(description=f"{emojis.loading} | Trying To Enable Nightmode", color=self.color))
        manageable_roles = [role for role in ctx.guild.roles if role.permissions.administrator and role.name != "@everyone" and role.position < ctx.guild.me.top_role.position]
        if not manageable_roles:
            return await ctx.send(embed=discord.Embed(description="No Roles Found With Administrator Permissions", color=self.color))
        for role in manageable_roles:
            admin_permissions = role.permissions
            permissions_bitfield = discord.Permissions(administrator=True).value
            if admin_permissions.administrator:
                try:
                    await sleep(3)
                    await role.edit(permissions=discord.Permissions(administrator=False), reason="RyZe Nightmode Enabled")
                    await add_role_to_nightmode(ctx.guild.id, role.id, permissions_bitfield)
                except Exception as e:
                    await ctx.send(embed=discord.Embed(description="Check My Role Permissions And Provide Me Proper Role.", color=self.color))
                    return
        await ctx.send(embed=discord.Embed(description="Nightmode enabled! Dangerous Permissions Disabled For Manageable Roles.", color=self.color))

    @nightmode.command(aliases=["off"])
    @nightmode_check()
    async def disable(self, ctx):
        await ctx.send(embed=discord.Embed(description=f"{emojis.loading} | Trying To Enable Nightmode", color=self.color))
        roles = await get_nightmode_roles(ctx.guild.id)
        for ryze in roles:
            ryze_role = ctx.guild.get_role(int(ryze['role_id']))
            if ryze_role:
                try:
                    await sleep(3)
                    await ryze_role.edit(permissions=discord.Permissions(ryze['admin_permissions']), reason='RyZe Nightmode Disabled')
                    await remove_role_from_nightmode(ctx.guild.id, ryze_role.id)
                except Exception as e:
                    continue
            else:
                await remove_role_from_nightmode(ctx.guild.id, ryze_role.id)
        await ctx.send(embed=discord.Embed(description="Nightmode disabled! Restored Permissions For Manageable Roles.", color=self.color))


async def setup(client):
    await client.add_cog(Nightmode(client))