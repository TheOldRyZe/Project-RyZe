import discord
from discord.ext import commands
from typing import Optional, Union

import settings.config as config
import settings.links as links
import settings.webhooks as webhooks

from structures.utils import *
from structures.checks import *

from paginators.np_list import *
from paginators.np_clear import *
from paginators.np_access_list import *
from paginators.np_access_clear import *
from paginators.bl_clear import *

from database.database import *


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = config.color

    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner Cog is Ready")

    @commands.group(aliases=["np"], invoke_without_command=True)
    @is_owner_or_noprefix_accessor()
    async def noprefix(self, ctx):
        embed = discord.Embed(
            title="No-Prefix Command Help",
            description="Use these commands to manage No-Prefix settings:",
            color=self.color,
        )
        embed.add_field(name="np add", value="Add a User To No-Prefix", inline=False)
        embed.add_field(
            name="np remove", value="Remove a User From No-Prefix", inline=False
        )
        embed.add_field(
            name="np list", value="List all Users in No-Prefix", inline=False
        )
        embed.add_field(
            name="np clear", value="Clear all Users from No-Prefix", inline=False
        )
        embed.add_field(
            name="np access", value="No-Prefix Access Help Group", inline=False
        )

        embed.set_footer(
            text="Requested by {}".format(ctx.author.display_name),
            icon_url=links.bot_avatar,
        )
        await ctx.send(embed=embed)

    @noprefix.command()
    @is_owner_or_noprefix_accessor()
    async def add(self, ctx, user: discord.User):
        user_id = str(user.id)
        RyZe = await add_user_to_noprefix(user_id)
        if RyZe:
            title = "No-Prefix Added"
            description = f"{user.mention} has been added to the No-Prefix list."
        else:
            title = "Error"
            description = f"{user.mention} is already in the No-Prefix list."

        embed = discord.Embed(
            title=title,
            description=description,
            color=self.color,
        )
        embed.set_footer(
            text=f"Added by {ctx.author.display_name}", icon_url=ctx.author.avatar.url
        )

        await ctx.send(embed=embed)
        embed = discord.Embed(description=f"**No-Prefix Added:**", color=self.color)
        embed.add_field(name="Added By:", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name="Added To:", value=f"{user.mention}", inline=False)
        embed.set_thumbnail(url=links.bot_avatar)
        if RyZe:
            await send_to_webhook(webhooks.noprefix_logs, embed)
        else:
            pass

    @noprefix.command()
    @is_owner_or_noprefix_accessor()
    async def remove(self, ctx, user: discord.User):
        user_id = str(user.id)
        RyZe = await remove_user_from_noprefix(user_id)
        if RyZe:
            title = "No-Prefix Removed"
            description = f"{user.mention} has been Removed From the No-Prefix list."
        else:
            title = "Error"
            description = f"{user.mention} is Not in the No-Prefix list."
        embed = discord.Embed(
            title=title,
            description=description,
            color=self.color,
        )
        embed.set_footer(
            text=f"Removed by {ctx.author.display_name}", icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)
        embed = discord.Embed(description=f"**No-Prefix Removed:**", color=self.color)
        embed.add_field(name="Removed By:", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name="Removed From:", value=f"{user.mention}", inline=False)
        embed.set_thumbnail(url=links.bot_avatar)
        if RyZe:
            await send_to_webhook(webhooks.noprefix_logs, embed)
        else:
            pass

    @noprefix.command()
    @is_owner_or_noprefix_accessor()
    async def list(self, ctx):
        noprefix_users = await get_noprefix_users()
        if not noprefix_users:
            embed = discord.Embed(
                description="No users found in the No-Prefix list.", color=self.color
            )
            await ctx.send(embed=embed)
            return

        pages = [noprefix_users[i : i + 10] for i in range(0, len(noprefix_users), 10)]
        current_page = 0

        formatted_users = []
        for num, user_id in enumerate(pages[current_page], start=current_page * 10 + 1):
            user = self.client.get_user(int(user_id)) or "User Not Found"
            formatted_users.append(f"**[{num}. {user}]({links.support_link})**")

        embed = discord.Embed(
            title=f"No-Prefix Users - Page {current_page + 1}/{len(pages)}",
            color=self.color,
        )
        embed.description = "\n".join(formatted_users)
        embed.set_thumbnail(url=links.bot_avatar)
        np_view = NoprefixButtons(ctx, pages, self.client)
        message = await ctx.send(embed=embed, view=np_view)
        np_view.message = message

    @noprefix.command()
    @is_owner_or_noprefix_accessor()
    async def clear(self, ctx):
        view = noPrefixClearButtons(ctx, self.client)
        confirmation_message = await ctx.send(
            embed=discord.Embed(
                description="Are you sure you want to clear all users from the No-Prefix list? This action cannot be undone.",
                color=self.color,
            ),
            view=view,
        )
        view.message = confirmation_message

    @noprefix.group(invoke_without_command=True)
    @is_owner()
    async def access(self, ctx):
        embed = discord.Embed(
            title="No-Prefix Access Help",
            description="Use these commands to manage No-Prefix Accesss settings:",
            color=self.color,
        )
        embed.add_field(
            name="np access add", value="Add a User To No-Prefix Access", inline=False
        )
        embed.add_field(
            name="np access remove",
            value="Remove a User From No-Prefix Access",
            inline=False,
        )
        embed.add_field(
            name="np access list",
            value="List all Users in No-Prefix Access",
            inline=False,
        )
        embed.add_field(
            name="np access reset",
            value="Reset No-Prefix Access Settings",
            inline=False,
        )

        embed.set_footer(
            text="Requested by {}".format(ctx.author.display_name),
            icon_url=links.bot_avatar,
        )
        await ctx.send(embed=embed)

    @access.command(name="add")
    @is_owner()
    async def _add(self, ctx, user: discord.User):
        user_id = str(user.id)
        RyZe = await add_user_to_noprefix_access(user_id)
        if RyZe:
            title = "No-Prefix Access Added"
            description = f"{user.mention} has been added to the No-Prefix Access list."
        else:
            title = "Error"
            description = f"{user.mention} is already in the No-Prefix Access list."

        embed = discord.Embed(
            title=title,
            description=description,
            color=self.color,
        )
        embed.set_footer(
            text=f"Added by {ctx.author.display_name}", icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)
        embed = discord.Embed(
            description=f"**No-Prefix Access Added:**", color=self.color
        )
        embed.add_field(name="Added By:", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name="Added To:", value=f"{user.mention}", inline=False)
        embed.set_thumbnail(url=links.bot_avatar)
        if RyZe:
            await send_to_webhook(webhooks.noprefix_logs, embed)
        else:
            pass

    @access.command(name="remove")
    @is_owner()
    async def _remove(self, ctx, user: discord.User):
        user_id = str(user.id)
        RyZe = await remove_user_from_noprefix_access(user_id)
        if RyZe:
            title = "No-Prefix Access Removed"
            description = (
                f"{user.mention} has been Removed From the No-Prefix Access list."
            )
        else:
            title = "Error"
            description = f"{user.mention} is Not in the No-Prefix Access list."
        embed = discord.Embed(
            title=title,
            description=description,
            color=self.color,
        )
        embed.set_footer(
            text=f"Removed by {ctx.author.display_name}", icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)
        embed = discord.Embed(
            description=f"**No-Prefix Access Removed:**", color=self.color
        )
        embed.add_field(name="Removed By:", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name="Removed From:", value=f"{user.mention}", inline=False)
        embed.set_thumbnail(url=links.bot_avatar)
        if RyZe:
            await send_to_webhook(webhooks.noprefix_logs, embed)
        else:
            pass

    @access.command(name="list")
    @is_owner()
    async def _list(self, ctx):
        noprefix_users = await get_noprefix_access_users()
        if not noprefix_users:
            embed = discord.Embed(
                description="No users found in the No-Prefix Access list.",
                color=self.color,
            )
            await ctx.send(embed=embed)
            return

        pages = [noprefix_users[i : i + 10] for i in range(0, len(noprefix_users), 10)]
        current_page = 0

        formatted_users = []
        for num, user_id in enumerate(pages[current_page], start=current_page * 10 + 1):
            user = self.client.get_user(int(user_id)) or "User Not Found"
            formatted_users.append(f"**[{num}. {user}]({links.support_link})**")

        embed = discord.Embed(
            title=f"No-Prefix Access Users - Page {current_page + 1}/{len(pages)}",
            color=self.color,
        )
        embed.description = "\n".join(formatted_users)
        embed.set_thumbnail(url=links.bot_avatar)
        np_view = noPrefixAccessListButtons(ctx, pages, self.client)
        message = await ctx.send(embed=embed, view=np_view)
        np_view.message = message

    @access.command(name="clear")
    @is_owner()
    async def _clear(self, ctx):
        view = noPrefixAccessClearButtons(ctx, self.client)
        confirmation_message = await ctx.send(
            embed=discord.Embed(
                description="Are you sure you want to clear all users from the No-Prefix Access list? This action cannot be undone.",
                color=self.color,
            ),
            view=view,
        )
        view.message = confirmation_message

    @commands.group(aliases=["bl"], invoke_without_command=True)
    @is_owner()
    async def blacklist(self, ctx):
        embed = discord.Embed(
            title="Blacklist Command Help",
            description="Use these commands To Blacklist:",
            color=self.color,
        )
        embed.add_field(
            name="bl add [user/guild]", value="Add a Value To Blacklist", inline=False
        )
        embed.add_field(
            name="bl remove [user/guild]",
            value="Remove a Value From Blacklist",
            inline=False,
        )
        embed.add_field(
            name="bl clear [user/guild]",
            value="Clear all Values from Blacklist",
            inline=False,
        )
        embed.set_footer(
            text="Requested by {}".format(ctx.author.display_name),
            icon_url=links.bot_avatar,
        )
        await ctx.send(embed=embed)

    @blacklist.command(name="add")
    @is_owner()
    async def _add_(self, ctx, type: str, value: Union[discord.User, int]):
        if type == "user":
            if isinstance(value, discord.User):
                user_id = str(value.id)
                lol = await add_to_blacklist(id=user_id, blacklist_type="user")
                if lol:
                    title = "Blacklist Added"
                    description = f"{value.mention} has been added to Blacklist."
                else:
                    title = "Error"
                    description = f"{value.mention} is already Blacklisted."

                embed = discord.Embed(
                    title=title,
                    description=description,
                    color=self.color,
                )
                embed.set_footer(
                    text=f"Added by {ctx.author.display_name}",
                    icon_url=ctx.author.avatar.url,
                )
                await ctx.send(embed=embed)
                embed = discord.Embed(
                    description=f"**Blacklist Added:**", color=self.color
                )
                embed.add_field(
                    name="Added By:", value=f"{ctx.author.mention}", inline=False
                )
                embed.add_field(
                    name="Added To:", value=f"{value.mention}", inline=False
                )
                embed.set_thumbnail(url=links.bot_avatar)
                if lol:
                    return await send_to_webhook(webhooks.blacklist_logs, embed)
                else:
                    return
        elif type == "guild":
            if isinstance(value, int):
                guild_id = str(value)
                lol = await add_to_blacklist(id=guild_id, blacklist_type="guild")
                if lol:
                    title = "Blacklist Added"
                    description = f"The Guild has been added to Blacklist."
                else:
                    title = "Error"
                    description = f"The Guild is already Blacklisted."

                embed = discord.Embed(
                    title=title,
                    description=description,
                    color=self.color,
                )
                embed.set_footer(
                    text=f"Added by {ctx.author.display_name}",
                    icon_url=ctx.author.avatar.url,
                )
                await ctx.send(embed=embed)
                embed = discord.Embed(
                    description=f"**Blacklist Added:**", color=self.color
                )
                embed.add_field(
                    name="Added By:", value=f"{ctx.author.mention}", inline=False
                )
                embed.add_field(
                    name="Added To:", value=f"Guild ID: `{value}`", inline=False
                )
                embed.set_thumbnail(url=links.bot_avatar)
                if lol:
                    return await send_to_webhook(webhooks.blacklist_logs, embed)
                else:
                    return
        embed = discord.Embed(
            description="Invalid type or value provided for the blacklist command.",
            color=self.color,
        )
        await ctx.send(embed=embed)

    @blacklist.command(name="remove")
    @is_owner()
    async def _remove_(self, ctx, type: str, value: Union[discord.User, int]):
        if type == "user":
            if isinstance(value, discord.User):
                user_id = str(value.id)
                lol = await remove_from_blacklist(id=user_id, blacklist_type="user")
                if lol:
                    title = "Blacklist Removed"
                    description = f"{value.mention} has been Removed From Blacklist."
                else:
                    title = "Error"
                    description = f"{value.mention} is Not Blacklisted."

                embed = discord.Embed(
                    title=title,
                    description=description,
                    color=self.color,
                )
                embed.set_footer(
                    text=f"Removed by {ctx.author.display_name}",
                    icon_url=ctx.author.avatar.url,
                )
                await ctx.send(embed=embed)
                embed = discord.Embed(
                    description=f"**Blacklist Removed:**", color=self.color
                )
                embed.add_field(
                    name="Removed By:", value=f"{ctx.author.mention}", inline=False
                )
                embed.add_field(
                    name="Removed From:", value=f"{value.mention}", inline=False
                )
                embed.set_thumbnail(url=links.bot_avatar)
                if lol:
                    return await send_to_webhook(webhooks.blacklist_logs, embed)
                else:
                    return
        elif type == "guild":
            if isinstance(value, int):
                guild_id = str(value)
                lol = await remove_from_blacklist(id=guild_id, blacklist_type="guild")
                if lol:
                    title = "Blacklist Removed"
                    description = f"The Guild has been Removed From Blacklist."
                else:
                    title = "Error"
                    description = f"The Guild is Not Blacklisted."

                embed = discord.Embed(
                    title=title,
                    description=description,
                    color=self.color,
                )
                embed.set_footer(
                    text=f"Removed by {ctx.author.display_name}",
                    icon_url=ctx.author.avatar.url,
                )
                await ctx.send(embed=embed)
                embed = discord.Embed(
                    description=f"**Blacklist Removed:**", color=self.color
                )
                embed.add_field(
                    name="Removed By:", value=f"{ctx.author.mention}", inline=False
                )
                embed.add_field(
                    name="Removed From:", value=f"Guild ID: `{value}`", inline=False
                )
                embed.set_thumbnail(url=links.bot_avatar)
                if lol:
                    return await send_to_webhook(webhooks.blacklist_logs, embed)
                else:
                    return
        embed = discord.Embed(
            description="Invalid type or value provided for the blacklist command.",
            color=self.color,
        )
        await ctx.send(embed=embed)

    @blacklist.command(name="clear")
    @is_owner()
    async def _clear_(self, ctx, type: Optional[str] = None):
        if type is None:
            embed = discord.Embed(
                description="Please specify whether you want to clear user or guild blacklist.",
                color=self.color,
            )
            return await ctx.send(embed=embed)

        if type.lower() not in ["user", "guild"]:
            embed = discord.Embed(
                description="Invalid type provided. Please specify user or guild.",
                color=self.color,
            )
            return await ctx.send(embed=embed)

        view = blacklistClearButtons(ctx, self.client, type)
        confirmation_message = await ctx.send(
            embed=discord.Embed(
                description="Are you sure you want to clear all Values from the Blacklist? This action cannot be undone.",
                color=self.color,
            ),
            view=view,
        )
        view.message = confirmation_message

    @commands.command(name="mongodb", aliases=["db"], hidden=True)
    @is_owner()
    async def mongo(self, ctx, *, query: str):
        try:
            cluster = database_instance()
            database = cluster["RyZe"]
            result = eval(query, {"db": database})

            if isinstance(result, pymongo.cursor.Cursor):
                formatted_results = [f"{doc}" for doc in result]

                embed = discord.Embed(
                    title="Query Execution Result",
                    description=f"\n```{formatted_results}```",
                    color=self.color,
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Query Execution Result",
                    description=f"\n```{result}```",
                    color=self.color,
                )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error", description=f"\n```{e}```", color=self.color
            )
            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Owner(client))
