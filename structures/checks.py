import discord
from discord.ext import commands

from structures.utils import *

import settings.config as config
import settings.credentials as credentials
import settings.emojis as emojis

def is_owner_or_noprefix_accessor():
    async def predicate(ctx):
        if ctx.author.id in credentials.owners:
            return True
        if await is_user_noprefix_accessor(ctx.author.id):
            return True
        embed = discord.Embed(
            description=f"{emojis.cross} | You do not have permission to use this command.",
            color=config.color,
        )
        await ctx.send(embed=embed)
        return False

    return commands.check(predicate)


def is_owner():
    async def predicate(ctx):
        if ctx.author.id in credentials.owners:
            return True
        embed = discord.Embed(
            description=f"{emojis.cross} | You do not have permission to use this command.",
            color=config.color,
        )
        await ctx.send(embed=embed)
        return False

    return commands.check(predicate)


def antinuke_enable_check():
    async def predicate(ctx):
        if (
            ctx.author.id == ctx.guild.owner.id
            or await is_extraowner(ctx.guild.id, ctx.author.id)
            or ctx.author.id in credentials.owners
        ):
            return True
        embed = discord.Embed(
            description=f"{emojis.cross} | You do not have permission to use this command.",
            color=config.color,
        )
        await ctx.send(embed=embed)
        return False

    return commands.check(predicate)


def antinuke_check():
    async def predicate(ctx):
        antinuke_check = await antinuke_status(ctx.guild.id)
        if antinuke_check != True:
            embed = discord.Embed(
                description=f"{emojis.cross} | Enable Antinuke First To Use This Command!",
                color=config.color,
            )
            await ctx.send(embed=embed)
            return False
        if (
            ctx.author.id == ctx.guild.owner.id
            or await is_extraowner(ctx.guild.id, ctx.author.id)
            or ctx.author.id in credentials.owners
        ):
            return True
        embed = discord.Embed(
            description=f"{emojis.cross} | You do not have permission to use this command.",
            color=config.color,
        )
        await ctx.send(embed=embed)
        return False

    return commands.check(predicate)


def extraowner_check():
    async def predicate(ctx):
        antinuke_check = await antinuke_status(ctx.guild.id)
        if antinuke_check != True:
            embed = discord.Embed(
                description=f"{emojis.cross} | Enable Antinuke First To Use This Command!",
                color=config.color,
            )
            await ctx.send(embed=embed)
            return False
        if (ctx.author.id == ctx.guild.owner.id
            or ctx.author.id in credentials.owners):
            return True
        embed = discord.Embed(
            description=f"{emojis.cross} | You do not have permission to use this command.",
            color=config.color,
        )
        await ctx.send(embed=embed)
        return False

    return commands.check(predicate)


def mainrole_check():
    async def predicate(ctx):
        antinuke_check = await antinuke_status(ctx.guild.id)
        if antinuke_check != True:
            embed = discord.Embed(
                description=f"{emojis.cross} | Enable Antinuke First To Use This Command!",
                color=config.color,
            )
            await ctx.send(embed=embed)
            return False
        if (ctx.author.id == ctx.guild.owner.id
            or await is_extraowner(ctx.guild.id, ctx.author.id)
            or ctx.author.id in credentials.owners):
            return True
        embed = discord.Embed(
            description=f"{emojis.cross} | You do not have permission to use this command.",
            color=config.color,
        )
        await ctx.send(embed=embed)
        return False

    return commands.check(predicate)


def whitelist_check():
    async def predicate(ctx):
        antinuke_check = await antinuke_status(ctx.guild.id)
        if antinuke_check != True:
            embed = discord.Embed(
                description=f"{emojis.cross} | Enable Antinuke First To Use This Command!",
                color=config.color,
            )
            await ctx.send(embed=embed)
            return False
        if (ctx.author.id == ctx.guild.owner.id
            or await is_extraowner(ctx.guild.id, ctx.author.id)
            or ctx.author.id in credentials.owners):
            return True
        embed = discord.Embed(
            description=f"{emojis.cross} | You do not have permission to use this command.",
            color=config.color,
        )
        await ctx.send(embed=embed)
        return False

    return commands.check(predicate)

def nightmode_check():
    async def predicate(ctx):
        if (ctx.author.id == ctx.guild.owner.id
            or await is_extraowner(ctx.guild.id, ctx.author.id)
            or ctx.author.id in credentials.owners):
            return True
        embed = discord.Embed(
            description=f"{emojis.cross} | You do not have permission to use this command.",
            color=config.color,
        )
        await ctx.send(embed=embed)
        return False

    return commands.check(predicate)



async def antinuke_event_check(user, guild, module, client):
    whitelisted = await is_whitelisted(guild.id, user.id, module)
    check_antinuke = await antinuke_status(guild.id)
    if check_antinuke != True:
        return "Antinuke_Disabled"
    if guild.owner.id == user.id or user.id == client.user.id:
        return "Is_Guild_Owner"
    if whitelisted != True:
        return "Not_Whitelisted"