from discord.ext import commands
import discord
from datetime import datetime
import pytz

import sugar_db

class GuildUpdateEventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    
    # コグアンロード処理
    def cog_unload(self):
        return super().cog_unload()

    @commands.Cog.listener()
    async def on_ready(self):
        print('load event cog: GuildUpdateEventCog')
        super().__init__()  # this is now required in this context.

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        channel_list: list[int] = await sugar_db.get_log_channels(before.id)
        if len(channel_list) == 0:
            return
        embed_before: discord.Embed = discord.Embed(title='旧ギルド情報')
        embed_after: discord.Embed = discord.Embed(title='新ギルド情報')
        if before.name != after.name:
            embed_before.add_field(name='ギルド名', value=before.name)
            embed_after.add_field(name='ギルド名', value=after.name)
        if before.description != after.description:
            embed_before.add_field(name='説明', value=before.description)
            embed_after.add_field(name='説明', value=after.description)
        if before.icon != after.icon:
            embed_before.set_thumbnail(url=before.icon.url)
            embed_after.set_thumbnail(url=after.icon.url)
        if before.banner != after.banner:
            embed_before.set_image(url=before.banner.url)
            embed_after.set_image(url=after.banner.url)
        if before.splash != after.splash:
            embed_before.set_image(url=before.splash.url)
            embed_after.set_image(url=after.splash.url)
        if before.afk_channel != after.afk_channel:
            embed_before.add_field(name='AFKチャンネル', value=before.afk_channel.name)
            embed_after.add_field(name='AFKチャンネル', value=after.afk_channel.name)
        if before.afk_timeout != after.afk_timeout:
            embed_before.add_field(name='AFKタイムアウト', value=str(before.afk_timeout))
            embed_after.add_field(name='AFKタイムアウト', value=str(after.afk_timeout))
        if before.owner != after.owner:
            embed_before.add_field(name='オーナー', value=before.owner.display_name)
            embed_after.add_field(name='オーナー', value=after.owner.display_name)
        if before.default_notifications != after.default_notifications:
            embed_before.add_field(name='デフォルト通知設定', value=str(before.default_notifications))
            embed_after.add_field(name='デフォルト通知設定', value=str(after.default_notifications))
        
        now: str = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y年%m月%d日 %p%I時%M分%S秒')
        
        embed_after.set_footer(text=now)
        
        embed_list: list = [embed_before, embed_after]
        
        channel: discord.abc.GuildChannel
        for channel_id in channel_list:
            channel = before.get_channel(channel_id)
            if channel == None:
                continue

            await channel.send(content=f":pencil2: **" + now + " ギルド編集**", embeds=embed_list)


async def setup(bot: commands.Bot):
    await bot.add_cog(GuildUpdateEventCog(bot))