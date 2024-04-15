import discord

from structures.utils import *

import settings.config as config
import settings.emojis as emojis
import settings.links as links
import settings.webhooks as webhooks

class extraOwnersClear(discord.ui.View):
    def __init__(self, ctx, client, message=None):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.client = client
        self.message = message

    async def close_view(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=None)

    async def on_timeout(self) -> None:
        embed = discord.Embed(
            description="Timeout Reached!",
            color=config.color,
        )
        await self.message.edit(embed=embed, view=None)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            return True
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="You Can Not Use This Interaction.", color=config.color
                ),
                ephemeral=True,
            )
            return False

    @discord.ui.button(label=emojis.tick, style=discord.ButtonStyle.grey)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.interaction_check(interaction):
            await clear_extraowners(interaction.guild.id)
            await interaction.response.edit_message(
                embed=discord.Embed(
                    description="Cleared All Extraowners From The List",
                    color=config.color,
                ),
                view=None,
            )
        await self.close_view()

    @discord.ui.button(label=emojis.cross, style=discord.ButtonStyle.grey)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.interaction_check(interaction):
            await interaction.response.edit_message(
                embed=discord.Embed(
                    description="Canceled The Process!", color=config.color
                ),
                view=None,
            )
        await self.close_view()
