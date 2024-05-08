# -*- coding: utf-8 -*-
import os
import discord
import SecretVar

BOT_VERSION = "1.0.0"
BOT_MODULE = "discord.py"

DEBUGMODE = False
TOKEN = SecretVar.TOKEN

MYSQL_HOST = SecretVar.MYSQL_HOST
MYSQL_PORT = SecretVar.MYSQL_PORT
MYSQL_DB = SecretVar.MYSQL_DB
MYSQL_USER = SecretVar.MYSQL_USER
MYSQL_PASSWORD = SecretVar.MYSQL_PASSWORD

if os.path.exists("D:\monster2408"):
    DEBUGMODE = True
    TOKEN = SecretVar.DEBUG_TOKEN
    
    MYSQL_HOST = SecretVar.MYSQL_DEBUG_HOST
    MYSQL_PORT = SecretVar.MYSQL_DEBUG_PORT
    MYSQL_DB = SecretVar.MYSQL_DEBUG_DB
    MYSQL_USER = SecretVar.MYSQL_DEBUG_USER
    MYSQL_PASSWORD = SecretVar.MYSQL_DEBUG_PASSWORD

TLANSLATION_DATA: dict[discord.Locale, dict[str, str]] = {
    discord.Locale.japanese: {
        "sugar": "sugar",
        'Registers the current channel as a monitoring log channel.': '現在のチャンネルを監視ログチャンネルに登録します。',
        'Connection to database failed.': 'データベースへの接続に失敗しました。',
        'Failed to register in database.': 'データベースへの登録に失敗しました。',
        'Database creation failed.': 'データベースの作成に失敗しました。',
    },
}

FMT_TLANSLATION_DATA: dict[discord.Locale, dict[str, str]] = {
    discord.Locale.japanese: {
        'I have registered {channel} in the monitoring log channel.': '{channel}を監視ログチャンネルに登録しました。',
        '{channel} is already registered.': '{channel}はすでに登録されています。',
    }
}