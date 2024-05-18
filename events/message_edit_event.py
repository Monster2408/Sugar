from discord.ext import commands
import discord
from datetime import datetime
import datetime
import sugar_db
from discord import app_commands

class MessageEditEventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    
    # コグアンロード処理
    def cog_unload(self):
        return super().cog_unload()

    @commands.Cog.listener()
    async def on_ready(self):
        print('load event cog: MessageEditEventCog')
        super().__init__()  # this is now required in this context.

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        channel_list: list[int] = await sugar_db.get_log_channels(payload.guild_id)
        if len(channel_list) == 0:
            return
                
        if 'embeds' in payload.data:
            if len(payload.data['embeds']) != 0:
                return
        msg = ' '
        # TODO: メッセージのキャッシュがない場合の処理作成中
        if payload.cached_message == None:
            return
        
        before_message: discord.Message = payload.cached_message
        msg_text: str = before_message.content
        if msg_text == '': msg_text = 'メッセージ本文無し'
        embed_before: discord.Embed = discord.Embed(title="旧メッセージ", description=msg_text)
        
        info_data: str = 'チャンネル: #' + before_message.channel.name + '(' + str(before_message.channel.id) + ')\nメッセージ: ' + str(before_message.id)
        info_data += '\nリンク: [メッセージリンク](' + before_message.jump_url + ')'
        embed_before.add_field(name='情報', value=info_data)
        
        date_before: datetime.datetime
        if before_message.edited_at != None:
            date_before = before_message.edited_at
        else:
            date_before = before_message.created_at
        date_before = date_before + datetime.timedelta(hours=9)
        date_before_str: str = date_before.strftime('%Y/%m/%d %p%I:%M:%S')
        embed_before.set_footer(text=date_before_str)
        
        name: str = before_message.author.display_name
        url: str = before_message.author.avatar.url
        embed_before.set_author(name=name, icon_url=url)
        
        after_message: discord.Message = await before_message.channel.fetch_message(before_message.id)
        msg_text = after_message.content
        if msg_text == '': msg_text = 'メッセージ本文無し'
        embed_after: discord.Embed = discord.Embed(title="新メッセージ", description=msg_text)
        
        info_data = 'チャンネル: #' + after_message.channel.name + '(' + str(after_message.channel.id) + ')\nメッセージ: ' + str(after_message.id)
        info_data += '\nリンク: [メッセージリンク](' + after_message.jump_url + ')'
        embed_after.add_field(name='情報', value=info_data)
        
        date_after: datetime.datetime = after_message.edited_at + datetime.timedelta(hours=9)
        
        date_after_str: str = date_after.strftime('%Y/%m/%d %p%I:%M:%S')
        embed_after.set_footer(text=date_after_str)
        
        embed_after.set_author(name=name, icon_url=url)
                
        embed_list: list = [embed_before, embed_after]
        
        guild: discord.Guild = self.bot.get_guild(payload.guild_id)
        channel: discord.abc.GuildChannel
        for channel_id in channel_list:
            channel = guild.get_channel(channel_id)
            if channel == None:
                continue

            await channel.send(content=f":pencil2: **" + date_after_str + " メッセージ編集**", embeds=embed_list)


async def setup(bot: commands.Bot):
    await bot.add_cog(MessageEditEventCog(bot))