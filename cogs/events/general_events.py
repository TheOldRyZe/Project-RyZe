import discord
from discord.ext import commands
import datetime

from structures.utils import *
from structures.checks import *

import settings.config as config
import settings.links as links
import settings.webhooks as webhooks

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = config.color

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events Cog is Ready")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if await is_blacklisted(
                str(message.author.id), 
                "user"
            ) or await is_blacklisted(
                str(message.guild.id), 
                "guild"
                ):
                return
            prefix = await get_guild_prefix(message.guild.id)
            if message.content == self.client.user.mention:
                embed = discord.Embed(
                    description=f"**Hey {message.author.mention},\nGuild Prefix: `{prefix}`\nGuild ID: `{message.guild.id}`**\n\n**[Invite Me]({links.invite_link}) | [Support Server]({links.support_link})\nTo See My All Commands Use `{prefix}help`**",
                    color=self.color
                )
                embed.set_thumbnail(url=message.author.avatar)
                embed.set_image(url=self.client.utils.get_random_bot_banner())
                embed.set_footer(text="Made By RyZe", icon_url=links.bot_avatar)
                embed.set_author(
                    name=message.author.name, icon_url=message.author.display_avatar.url
                )
                view = await common_buttons()
                await message.reply(
                    embed=embed, 
                    view=view, 
                    mention_author=False)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.author == self.client.user:
            return
        
        embed = discord.Embed(title="Command Logger", color=self.color)
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.add_field(name="Command", value=f"`{ctx.command}`", inline=False)
        embed.add_field(name="Author", value=f"{ctx.author.mention}", inline=True)
        embed.add_field(name="Guild", value=f"{ctx.guild.name}", inline=True)
        embed.add_field(name="Channel", value=f"{ctx.channel.mention}", inline=True)
        embed.add_field(name="Message", value=f"```{ctx.message.content}```", inline=False)
        embed.set_footer(text=f"{datetime.date.today()} | {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        await send_to_webhook(webhooks.command_logs, embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandNotFound):
            return
        await error_logger(error)


async def setup(client):
    await client.add_cog(Events(client))
