from discord.ext import commands
import discord

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
        before_embed: discord.Embed = discord.Embed(title='旧ギルド情報')
        after_embed: discord.Embed = discord.Embed(title='新ギルド情報')
        if before.name != after.name:
            before_embed.add_field(name='ギルド名', value=before.name)
            after_embed.add_field(name='ギルド名', value=after.name)
        if before.description != after.description:
            before_embed.add_field(name='説明', value=before.description)
            after_embed.add_field(name='説明', value=after.description)
        if before.icon != after.icon:
            before_embed.set_thumbnail(url=before.icon.url)
            after_embed.set_thumbnail(url=after.icon.url)
        if before.banner != after.banner:
            before_embed.set_image(url=before.banner.url)
            after_embed.set_image(url=after.banner.url)
        if before.splash != after.splash:
            before_embed.set_image(url=before.splash.url)
            after_embed.set_image(url=after.splash.url)
        if before.afk_channel != after.afk_channel:
            before_embed.add_field(name='AFKチャンネル', value=before.afk_channel.name)
            after_embed.add_field(name='AFKチャンネル', value=after.afk_channel.name)
        if before.afk_timeout != after.afk_timeout:
            before_embed.add_field(name='AFKタイムアウト', value=str(before.afk_timeout))
            after_embed.add_field(name='AFKタイムアウト', value=str(after.afk_timeout))
        if before.owner != after.owner:
            before_embed.add_field(name='オーナー', value=before.owner.display_name)
            after_embed.add_field(name='オーナー', value=after.owner.display_name)
        if before.default_notifications != after.default_notifications:
            before_embed.add_field(name='デフォルト通知設定', value=str(before.default_notifications))
            after_embed.add_field(name='デフォルト通知設定', value=str(after.default_notifications))
        

async def setup(bot: commands.Bot):
    await bot.add_cog(GuildUpdateEventCog(bot))