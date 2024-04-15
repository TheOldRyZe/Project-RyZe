import discord
from discord.ext import commands

from structures.utils import *
from structures.checks import *

from paginators.mainrole_clear import *

import settings.config as config
import settings.links as links


from database.database import *


class Mainrole(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = config.color

    @commands.Cog.listener()
    async def on_ready(self):
        print("Antinuke : Mainrole is Ready")
    
    @commands.group(aliases=["mr"], invoke_without_command=True)
    async def mainrole(self, ctx):
        embed = discord.Embed(
            title="Mainrole Command Help",
            description="Use these commands to manage Mainrole settings:",
            color=self.color,
        )
        embed.add_field(
            name="mainrole add", value="Add's A Mainrole", inline=False
        )
        embed.add_field(
            name="mainrole remove", value="Remove's A Mainrole", inline=False
        )
        embed.add_field(
            name="mainrole clear", value="Clear's All Mainroles", inline=False
        )
        embed.add_field(
            name="mainrole list", value="Lists's All Mainroles", inline=False
        )
        embed.set_footer(
            text="Requested by {}".format(ctx.author.display_name),
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=embed)

    @mainrole.command(invoke_without_command=True)
    @mainrole_check()
    async def add(self, ctx, role: discord.Role):
        if role.position >= ctx.guild.me.top_role.position:
            return await ctx.send(embed=discord.Embed(description="I Can Not Set That Role As A MainRole!"))
        ryze = await add_mainrole(ctx.guild.id, role.id)
        if ryze == "maximum":
            embed = discord.Embed(
                description=f"{emojis.cross} | Maximum Number (5) of Mainroles Reached.",
                color=self.color,
            )
            await ctx.send(embed=embed)
        if ryze == "already":
            embed = discord.Embed(
                description=f"{emojis.cross} | {role.mention} is already a Mainrole.",
                color=self.color,
            )
            await ctx.send(embed=embed)
        if ryze == "added":
            embed = discord.Embed(
                description=f"{emojis.tick} | {role.mention} has been added to the Mainrole.",
                color=self.color,
            )
            await ctx.send(embed=embed)

    @mainrole.command()
    @mainrole_check()
    async def remove(self, ctx, role: discord.Role):
        result = await remove_mainrole(ctx.guild.id, role.id)
        if result == "removed":
            embed = discord.Embed(
                description=f"{emojis.tick} | {role.mention} has been removed from Mainroles.",
                color=self.color,
            )
        else:
            embed = discord.Embed(
                description=f"{emojis.cross} | {role.mention} is not a Mainrole.", color=self.color
            )
        await ctx.send(embed=embed)

    @mainrole.command()
    @mainrole_check()
    async def config(self, ctx):
        mainroles = await list_mainroles(ctx.guild.id)
        if mainroles:
            mainroles_mentions = [
                f"<@&{mainrole}>"
                for mainrole in mainroles
            ]
            embed = discord.Embed(
                title="Mainroles",
                description="\n".join(mainroles_mentions),
                color=self.color,
            )
        else:
            embed = discord.Embed(
                description=f"{emojis.cross} | No Mainroles configured.", color=self.color
            )
        await ctx.send(embed=embed)

    @mainrole.command()
    @mainrole_check()
    async def clear(self, ctx):
        view = MainroleClear(ctx, self.client)
        confirmation_message = await ctx.send(
            embed=discord.Embed(
                description="Are you sure you want to clear all users from the Mainroles? This action cannot be undone.",
                color=self.color,
            ),
            view=view,
        )
        view.message = confirmation_message

async def setup(client):
    await client.add_cog(Mainrole(client))