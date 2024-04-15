import discord
from discord.ext import commands

from structures.utils import *
from structures.checks import *

from paginators.whitelist_panel import *
from paginators.whitelist_config import *
from paginators.whitelist_clear import *

import settings.config as config
import settings.links as links


from database.database import *


class Whitelist(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = config.color

    @commands.Cog.listener()
    async def on_ready(self):
        print("Antinuke : Whitelist is Ready")


    @commands.group(aliases=["wl"], invoke_without_command=True)
    async def whitelist(self, ctx):
        embed = discord.Embed(
            title="Whitelist Command Help",
            description="Use these commands to manage Whitelist settings:",
            color=self.color,
        )
        embed.add_field(
            name="whitelist panel", value="Shows The Whitelist Panel", inline=False
        )
        embed.add_field(
            name="whitelist config", value="Show's All Whitelists", inline=False
        )
        embed.add_field(
            name="whitelist clear", value="Clear's All Whitelists", inline=False
        )
        embed.set_footer(
            text="Requested by {}".format(ctx.author.display_name),
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=embed)

    @whitelist.command()
    @whitelist_check()
    async def panel(self, ctx, user:discord.User):
        embed = discord.Embed(description="**Whitelisting this user will grant immunity from antinuke measures. You can view the current whitelists using the command: `whitelist config`**",color=self.color)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed.add_field(name = "Modules", value = await list_whitelists(ctx.guild.id, user.id))
        view = RyZeView(ctx, self.client, user)
        message = await ctx.reply(embed=embed, mention_author=False, view=view)
        view.message = message
    
    
    @whitelist.command()
    @whitelist_check()
    async def config(self, ctx):
        whitelisted_user_ids = await list_whitelisted_users(ctx.guild.id)
        if not whitelisted_user_ids:
            embed = discord.Embed(
                description="No users found in the Whitelist.", color=self.color
            )
            await ctx.send(embed=embed)
            return
        pages = [whitelisted_user_ids[i : i + 10] for i in range(0, len(whitelisted_user_ids), 10)]
        current_page = 0
        formatted_users = []
        for num, user_id in enumerate(pages[current_page], start=current_page * 10 + 1):
            user = self.client.get_user(int(user_id)) or "User Not Found"
            formatted_users.append(f"**[{num}. {user}]({links.support_link})**")
        embed = discord.Embed(
            title=f"Whitelisted Users - Page {current_page + 1}/{len(pages)}",
            color=self.color,
        )
        embed.description = "\n".join(formatted_users)
        embed.set_thumbnail(url=links.bot_avatar)
        view = WhitelistConfigButtons(ctx, pages, self.client)
        message = await ctx.send(embed=embed, view=view)
        view.message = message

    @whitelist.command()
    @whitelist_check()
    async def clear(self, ctx):
        view = WhitelistClear(ctx, self.client)
        confirmation_message = await ctx.send(
            embed=discord.Embed(
                description="Are you sure you want to clear all users from the Whitelist? This action cannot be undone.",
                color=self.color,
            ),
            view=view,
        )
        view.message = confirmation_message


async def setup(client):
    await client.add_cog(Whitelist(client))