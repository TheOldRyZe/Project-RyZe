import discord
from discord.ext import commands

from paginators.extraowners_clear import *

from structures.utils import *
from structures.checks import *

import settings.config as config
import settings.links as links


from database.database import *


class Extraowner(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = config.color

    @commands.Cog.listener()
    async def on_ready(self):
        print("Antinuke : Extraowner is Ready")

    @commands.group(invoke_without_command=True)
    async def extraowner(self, ctx):
        embed = discord.Embed(
            title="Extraowner Command Help",
            description="Use these commands to manage Extraowner settings:",
            color=self.color,
        )
        embed.add_field(
            name="extraowner add", value="Add's An Extraowner", inline=False
        )
        embed.add_field(
            name="extraowner remove", value="Remove's An Extraowner", inline=False
        )
        embed.add_field(
            name="extraowner config", value="Show's All Extraowners", inline=False
        )
        embed.add_field(
            name="extraowner clear", value="Clear's All Extraowners", inline=False
        )
        embed.set_footer(
            text="Requested by {}".format(ctx.author.display_name),
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=embed)

    @extraowner.command(invoke_without_command=True)
    @extraowner_check()
    async def add(self, ctx, user: discord.User):
        ryze = await add_extraowner(ctx.guild.id, user.id)
        if ryze == "maximum":
            embed = discord.Embed(
                description=f"{emojis.cross} | Maximum Number (5) of Extraowners Reached.",
                color=self.color,
            )
            await ctx.send(embed=embed)
        if ryze == "already":
            embed = discord.Embed(
                description=f"{emojis.cross} | {user.mention} is already an Extraowner.",
                color=self.color,
            )
            await ctx.send(embed=embed)
        if ryze == "added":
            embed = discord.Embed(
                description=f"{emojis.tick} | {user.mention} has been added to the Extraowner.",
                color=self.color,
            )
            await ctx.send(embed=embed)

    @extraowner.command()
    @extraowner_check()
    async def remove(self, ctx, user: discord.User):
        result = await remove_extraowner(ctx.guild.id, user.id)
        if result == "removed":
            embed = discord.Embed(
                description=f"{emojis.tick} | {user.mention} has been removed from Extraowners.",
                color=self.color,
            )
        else:
            embed = discord.Embed(
                description=f"{emojis.cross} | {user.mention} is not an Extraowner.", color=self.color
            )
        await ctx.send(embed=embed)

    @extraowner.command()
    @extraowner_check()
    async def config(self, ctx):
        extraowners = await list_extraowners(ctx.guild.id)
        if extraowners:
            extraowners_mentions = [
                f"[{self.client.get_user(extraowner) if not None else 'User Not Found'}]({links.support_link})"
                for extraowner in extraowners
            ]
            embed = discord.Embed(
                title="Extraowners",
                description="\n".join(extraowners_mentions),
                color=self.color,
            )
        else:
            embed = discord.Embed(
                description=f"{emojis.cross} | No Extraowners configured.", color=self.color
            )
        await ctx.send(embed=embed)

    @extraowner.command()
    @extraowner_check()
    async def clear(self, ctx):
        view = extraOwnersClear(ctx, self.client)
        confirmation_message = await ctx.send(
            embed=discord.Embed(
                description="Are you sure you want to clear all users from the Extraowners? This action cannot be undone.",
                color=self.color,
            ),
            view=view,
        )
        view.message = confirmation_message


async def setup(client):
    await client.add_cog(Extraowner(client))
