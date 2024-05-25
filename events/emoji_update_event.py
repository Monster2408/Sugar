from discord.ext import commands
import discord
from datetime import datetime
import pytz

import sugar_db
import sugar_translator

ADD_LOG_NAME_DICT = {
    discord.Locale.american_english: 'Emoji Add Log',
    discord.Locale.japanese: '絵文字追加ログ',
}

DELETE_LOG_NAME_DICT = {
    discord.Locale.american_english: 'Emoji Delete Log',
    discord.Locale.japanese: '絵文字削除ログ',
}

class EmojiUpdateEventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    
    # コグアンロード処理
    def cog_unload(self):
        return super().cog_unload()

    @commands.Cog.listener()
    async def on_ready(self):
        print('load event cog: EmojiUpdateEventCog')
        super().__init__()  # this is now required in this context.

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before: discord.Emoji, after: discord.Emoji):
        await self.bot.wait_until_ready()
        add_log_name: str = sugar_translator.translate(ADD_LOG_NAME_DICT, guild.preferred_locale)
        delete_log_name: str = sugar_translator.translate(DELETE_LOG_NAME_DICT, guild.preferred_locale)
        channel_list: list[int] = await sugar_db.get_log_channels(guild.id)
        if len(channel_list) == 0:
            return
        text = ""
        for emoji in set(before) ^ set(after):
            text += "{0}(ID:{1}) ".format(emoji.name, emoji.id)
        embed = discord.Embed(title="情報", description=text)
        log_name: str = add_log_name
        if len(before) > len(after):
            log_name=delete_log_name
        embed.set_author(name=log_name)
        now = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y年%m月%d日 %p%I時%M分%S秒')
        embed.set_footer(text=now)
        await sugar_db.send_log_channel(content=f":pencil2: **{now} {log_name}**", embed=embed, channel_list=channel_list, guild=guild)


async def setup(bot: commands.Bot):
    await bot.add_cog(EmojiUpdateEventCog(bot))