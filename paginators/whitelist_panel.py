import discord

from structures.utils import *

import settings.config as config
import settings.emojis as emojis
import settings.links as links
import settings.webhooks as webhooks




class RyZeView(discord.ui.View):
    def __init__(self, ctx, client, user, message=None):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.client = client
        self.message = message
        self.user = user

    async def on_timeout(self) -> None:
        try:
            await self.message.edit(view=None)
        except discord.errors.NotFound:
            return
        

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            return True
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="You can not use this Interaction.", color=config.color
                ),
                ephemeral=True,
            )
            return False

    @discord.ui.select(placeholder="Whitelist Specific Module", options=whitelist_options, min_values=1, max_values=len(whitelist_options))
    async def select_whitelist_module(self, interaction: discord.Interaction, select: discord.ui.Select):
        selected_values = select.values
        if selected_values:
            for value in selected_values:
                if value in whitelist_modules:
                    await toggle_whitelist_module(interaction.guild.id, self.user.id, value)
            embed = await get_whitelist_embed(interaction.guild.id, self.user.id, self.ctx)
            try:
                await interaction.response.edit_message(embed=embed)
            except discord.errors.NotFound:
                pass

    
    @discord.ui.button(label="Add This User To All Categories", style=discord.ButtonStyle.green)
    async def Add_To_All_Categories(self, interaction: discord.Interaction, button: discord.ui.Button):
        ryze = await add_whitelist(interaction.guild.id, self.user.id, "All")
        await sleep(2)
        if ryze:
            embed = await get_whitelist_embed(interaction.guild.id, self.user.id, self.ctx)
            try:
                await interaction.response.edit_message(embed=embed)
            except discord.errors.NotFound:
                pass
            
    @discord.ui.button(label="Remove This User From All Categories", style=discord.ButtonStyle.red)
    async def Remove_From_All_Categories(self, interaction: discord.Interaction, button: discord.ui.Button):
        ryze = await remove_whitelist(interaction.guild.id, self.user.id, "All")
        await sleep(2)
        if ryze:
            embed = await get_whitelist_embed(interaction.guild.id, self.user.id, self.ctx)
            try:
                await interaction.response.edit_message(embed=embed)
            except discord.errors.NotFound:
                pass