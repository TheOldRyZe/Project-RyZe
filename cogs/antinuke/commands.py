import discord
from discord.ext import commands

from structures.utils import *
from structures.checks import *

import settings.config as config
import settings.links as links


from database.database import *


class Antinuke(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = config.color

    @commands.Cog.listener()
    async def on_ready(self):
        print("Antinuke : Commands is Ready")

    @commands.group(invoke_without_command=True)
    async def antinuke(self, ctx):
        embed = discord.Embed(
            title="Antinuke Command Help",
            description="Use these commands to manage Antinuke settings:",
            color=self.color,
        )
        embed.add_field(
            name="antinuke enable", value="Enable Antinuke feature", inline=False
        )
        embed.add_field(
            name="antinuke disable", value="Disable Antinuke feature", inline=False
        )
        embed.add_field(
            name="antinuke config", value="Show's Antinuke Config", inline=False
        )

        embed.set_footer(
            text="Requested by {}".format(ctx.author.display_name),
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=embed)

    @antinuke.command()
    @antinuke_enable_check()
    async def enable(self, ctx):
        result = await enable_antinuke(ctx.guild.id)
        if result == "already":
            embed = discord.Embed(
                description=f"{emojis.cross} | Antinuke is already enabled!", color=self.color
            )
            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url
            )
            await ctx.send(embed=embed)
        if result == "updated" or result == True:
            ryze = await antinuke_embed(ctx)
            await antinuke_role_setup(ctx)
            text = await list_antinuke_modules(ctx.guild.id)
            embed = discord.Embed(
                description="**It's essential for optimal performance that my role is placed at the top of the hierarchy list. This strategic positioning will enable me to contribute effectively for a Good Antiwizz**",
                color=self.color,
            )
            embed.set_thumbnail(url=links.bot_avatar)
            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.avatar.url
            )
            embed.add_field(
                name="Modules", value=text if not None else "ERROR", inline=False
            )
            view = await common_buttons()
            await ryze.edit(embed=embed, view=view)

    @antinuke.command()
    @antinuke_check()
    async def disable(self, ctx):
        result = await disable_antinuke(ctx.guild.id)
        if result == "already":
            embed = discord.Embed(
                description=f"{emojis.cross} | Antinuke is already disabled!", color=self.color
            )
            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url
            )
            await ctx.send(embed=embed)
        elif result == "updated" or result == True:
            embed = discord.Embed(
                description=f"{emojis.tick} | Antinuke has been disabled successfully!", color=self.color
            )
            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url
            )
            await ctx.send(embed=embed)

    @antinuke.command()
    @antinuke_check()
    async def config(self, ctx):
        config_data = await list_antinuke_modules(ctx.guild.id)
        if config_data:
            embed = discord.Embed(
                title="Antinuke Configuration",
                color=self.color,
            )
            embed.description = "**It's essential for optimal performance that my role is placed at the top of the hierarchy list. This strategic positioning will enable me to contribute effectively for a Good Antiwizz**"
            embed.set_thumbnail(url=links.bot_avatar)
            embed.add_field(name="Modules", value=config_data)
            embed.set_footer(
                text="Requested by {}".format(ctx.author.display_name),
                icon_url=ctx.author.avatar.url,
            )
            await ctx.send(embed=embed)


    
async def setup(client):
    await client.add_cog(Antinuke(client))
