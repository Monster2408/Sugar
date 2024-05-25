from discord.ext import commands
import discord
from datetime import datetime
import pytz

import sugar_db
import sugar_translator

LOG_NAME_DICT = {
    discord.Locale.american_english: 'Channel Delete Log',
    discord.Locale.japanese: 'チャンネル削除ログ',
}

class ChannelDeleteEventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    
    # コグアンロード処理
    def cog_unload(self):
        return super().cog_unload()

    @commands.Cog.listener()
    async def on_ready(self):
        print('load event cog: ChannelDeleteEventCog')
        super().__init__()  # this is now required in this context.

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, ch: discord.abc.GuildChannel):
        await self.bot.wait_until_ready()
        guild: discord.Guild = ch.guild
        log_name: str = sugar_translator.translate(LOG_NAME_DICT, guild.preferred_locale)
        channel_list: list[int] = await sugar_db.get_log_channels(guild.id)
        if len(channel_list) == 0:
            return
        em = discord.Embed(title="情報", description="チャンネル名: #{}\n".format(str(ch.name)) + "ID:{}".format(ch.id))
        em.set_author(name=log_name)
        now = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y年%m月%d日 %p%I時%M分%S秒')
        em.set_footer(text=now)
        await sugar_db.send_log_channel(content=f":pencil2: **{now} {log_name}**", embed=em, channel_list=channel_list, guild=guild)

async def setup(bot: commands.Bot):
    await bot.add_cog(ChannelDeleteEventCog(bot))