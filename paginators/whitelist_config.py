import discord

import settings.config as config
import settings.links as links
import settings.emojis as emojis


class WhitelistConfigButtons(discord.ui.View):
    def __init__(self, ctx, pages, client, message=None):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.pages = pages
        self.current_page = 0
        self.client = client
        self.message = message

    async def show_current_page(self, interaction):
        formatted_users = [
            f"**[{num}. {self.client.get_user(int(user_id)) or 'User Not Found'}]({links.support_link})**"
            for num, user_id in enumerate(
                self.pages[self.current_page], start=self.current_page * 10 + 1
            )
        ]
        embed = discord.Embed(
            title=f"Whitelisted Users - Page {self.current_page + 1}/{len(self.pages)}",
            color=config.color,
        )
        embed.description = "\n".join(formatted_users)
        embed.set_thumbnail(url=links.bot_avatar)
        await interaction.response.edit_message(embed=embed, view=self)

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

    async def on_timeout(self) -> None:
        try:
            await self.message.edit(view=None)
        except discord.errors.NotFound:
            return

    @discord.ui.button(emoji=emojis.first, style=discord.ButtonStyle.grey)
    async def first_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if await self.interaction_check(interaction):
            self.current_page = 0
            await self.show_current_page(interaction)

    @discord.ui.button(emoji=emojis.previous, style=discord.ButtonStyle.grey)
    async def previous_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if await self.interaction_check(interaction):
            self.current_page = max(0, self.current_page - 1)
            await self.show_current_page(interaction)

    @discord.ui.button(emoji=emojis.cross, style=discord.ButtonStyle.grey)
    async def delete(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if await self.interaction_check(interaction):
            await interaction.message.delete()

    @discord.ui.button(emoji=emojis.next, style=discord.ButtonStyle.grey)
    async def next_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if await self.interaction_check(interaction):
            self.current_page = min(len(self.pages) - 1, self.current_page + 1)
            await self.show_current_page(interaction)

    @discord.ui.button(emoji=emojis.last, style=discord.ButtonStyle.grey)
    async def last_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if await self.interaction_check(interaction):
            self.current_page = len(self.pages) - 1
            await self.show_current_page(interaction)
