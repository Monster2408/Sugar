from discord.ext import commands
import discord
from datetime import datetime
import datetime as dt
import pytz

import sugar_db
import sugar_translator

LOG_NAME_DICT = {
    discord.Locale.american_english: 'Channel Delete Log',
    discord.Locale.japanese: 'チャンネル削除ログ',
}

def getMessageData(msg: discord.Message) -> discord.Embed:
    if msg is None: return
    embed = discord.Embed(title="情報", description=msg.content)
    message_data: str = 'チャンネル: ' + msg.channel.name + '(' + str(msg.channel.id) + ') \ <#' + str(msg.channel.id) + '>'
    message_data += '\nメッセージ: ' + str(msg.id)
    message_data += '\n送信者: <@' + str(msg.author.id) + '>'
    time = msg.created_at + dt.timedelta(hours=9)
    message_data += '\n送信日時: ' + time.strftime('%Y年%m月%d日 %p%I時%M分%S秒')
    
    embed.add_field(name='その他', value=message_data)
    embed.set_author(name="メッセージ削除ログ")
    time = msg.created_at
    time = time = datetime.now(pytz.timezone('Asia/Tokyo'))
    text = '削除日時: ' + time.strftime('%Y年%m月%d日 %p%I時%M分%S秒')
    if msg.guild.icon != None: embed.set_footer(text=msg.guild.name + "\n" + text, icon_url=msg.guild.icon.url)
    else: embed.set_footer(text=msg.guild.name + "\n" + text)
    if msg.author.avatar != None: embed.set_author(name=msg.author.name, icon_url=msg.author.avatar.url)
    else: embed.set_author(name=msg.author.name)
    if msg.attachments:
        for attachment in msg.attachments:
            if attachment.url.endswith((".png", ".jpg", ".jpeg", ".gif")):
                embed.set_image(url=attachment.url)
                break
            else:
                for file_type in (".png?", ".jpg?", ".jpeg?", ".gif?"):
                    if file_type in attachment.url:
                        embed.set_image(url=attachment.url)
                        break
    return embed

class messageDeleteEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    
    # コグアンロード処理
    def cog_unload(self):
        return super().cog_unload()

    @commands.Cog.listener()
    async def on_ready(self):
        print('load event cog: MessageDeleteEventCog')
        super().__init__()  # this is now required in this context.

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(payload.channel_id)
        guild: discord.Guild = channel.guild
        log_name: str = sugar_translator.translate(LOG_NAME_DICT, guild.preferred_locale)
        channel_list: list[int] = await sugar_db.get_log_channels(guild.id)
        if len(channel_list) == 0:
            return
        msg_id = payload.message_id
        message: discord.Message = payload.cached_message
        if message == None: 
            message = discord.utils.get(self.bot.cached_messages, id=msg_id)
        msg = ' '
        if message == None:
            msg += '記録なし'
        elif len(message.content) == 0:
            msg += 'Embedですた'
        else:
            msg += message.content
        now = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y年%m月%d日 %p%I時%M分%S秒')
        
        msg_data: discord.Embed = getMessageData(message)
        
        await sugar_db.send_log_channel(content=f":wastebasket: **{now} {log_name}**", embed=msg_data, channel_list=channel_list, guild=guild)

async def setup(bot: commands.Bot):
    await bot.add_cog(messageDeleteEvent(bot))
