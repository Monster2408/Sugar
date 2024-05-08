# -*- coding: utf-8 -*-
from discord.ext import commands
import discord
from discord import app_commands
import sugar_db

class SugarCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # コグアンロード処理
    def cog_unload(self):
        return super().cog_unload()

    # テストコマンド
    @commands.Cog.listener()
    async def on_ready(self):
        print('load command cog: SugarCommandCog')
        super().__init__()  # this is now required in this context.

    @app_commands.command(
        name=app_commands.locale_str("sugar"), 
        description=app_commands.locale_str("Registers the current channel as a monitoring log channel.")
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def pardon(self, interaction: discord.Interaction):
        channel = interaction.channel
        response: int = await sugar_db.add_channel(channel)
        if response == -1:
            await interaction.response.send_message(app_commands.locale_str("Connection to database failed."))
        elif response == -2:
            default_msg = "{channel} is already registered."
            msg = await interaction.translate(app_commands.locale_str(
                default_msg,
                fmt_arg={
                    'channel' : channel, 
                },
            ))
            await interaction.response.send_message(msg or default_msg)
        elif response == -3:
            await interaction.response.send_message(app_commands.locale_str("Database creation failed."))
        elif response == -4:
            await interaction.response.send_message(app_commands.locale_str("Failed to register in database."))
        else:
            default_msg = "I have registered {channel} in the monitoring log channel."
            msg = await interaction.translate(app_commands.locale_str(
                default_msg,
                fmt_arg={
                    'channel' : channel, 
                },
            ))
            await interaction.response.send_message(msg or default_msg)

async def setup(bot: commands.Bot):
    await bot.add_cog(SugarCommandCog(bot))