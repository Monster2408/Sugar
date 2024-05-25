import discord

def translate(map: dict, locale: discord.Locale) -> str:
    return map.get(locale, map.get(0))