# -*- coding: utf-8 -*-
import discord
from discord import app_commands
from discord.ext import commands
import locale
locale.setlocale(locale.LC_ALL, '')
from datetime import datetime
import traceback 
import pytz
from japanera import EraDate
import asyncio

import Var

DEBUGMODE = False

CMD_COGS = [
    'cmds.sugar_cmd',
    # 'cmds.sync_cmd',
    # 'cmds.help_cmd',
]

EVENT_COGS = [
    'events.message_edit_event',
    'events.guild_update_event',
]

class MyTranslator(app_commands.Translator):
    async def translate(self, string: app_commands.locale_str, locale: discord.Locale, context: app_commands.TranslationContext):
        if 'fmt_arg' in string.extras:
            fmt = Var.FMT_TLANSLATION_DATA.get(locale, {}).get(string.message, string.message)
            return fmt.format(**(string.extras['fmt_arg']))
        return Var.TLANSLATION_DATA.get(locale, {}).get(string.message)

class MyBot(commands.Bot):
    def __init__(self, prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=prefix, intents=intents)

    async def setup_hook(self):
        for cog in CMD_COGS:
            try:
                await self.load_extension(cog)
            except Exception:
                traceback.print_exc()
        for cog in EVENT_COGS:
            try:
                await self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print(f'Sugarのバージョンはv{Var.BOT_VERSION}')
        time = datetime.now(pytz.timezone('Asia/Tokyo'))
        era_date = EraDate(int(time.strftime("%Y")), int(time.strftime("%m")), int(time.strftime("%d")))
        now = time.strftime(' %H時%M分%S秒')
        print('現在時刻 ' + era_date.strftime("%-E%-O年%m月%d日") + now)
        print(f'{Var.BOT_MODULE}のバージョンはv{discord.__version__}')
        print('-----')
        await self.wait_until_ready()
        await self.change_presence(status=discord.Status.online, activity=discord.Game(f"v{Var.BOT_VERSION}"))
        await self.tree.set_translator(MyTranslator())
        await self.tree.sync(guild=None)

async def main():    
    token = Var.TOKEN
    bot = MyBot(prefix='!?', intents=discord.Intents.all())
    await bot.start(token=token)

if __name__ == '__main__':
    asyncio.run(main())