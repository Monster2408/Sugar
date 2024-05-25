# -*- coding: utf-8 -*-
import discord
import Var
import mysql.connector
from discord import app_commands

async def add_channel(channel: discord.abc.GuildChannel) -> int:
    # DBへ接続
    conn = mysql.connector.connect(
        user=Var.MYSQL_USER,
        password=Var.MYSQL_PASSWORD,
        host=Var.MYSQL_HOST,
        port=Var.MYSQL_PORT,
        database=Var.MYSQL_DB
    )
    
    # DBの接続確認
    if not conn.is_connected():
        return -1
    
    cur = conn.cursor()
    try:
        # テーブル作成
        create_table_sql: str = """create table if not exists channel_ids (
                id bigint(20) not null auto_increment primary key,
                guild_id bigint(20) not null
            );"""
        cur.execute(create_table_sql)
        conn.commit()
    except Exception as e:
        print(e)
        return -3
    # チャネルIDが既に登録されているか確認
    check_sql = f"select id from channel_ids where id = {str(channel.id)};"
    cur.execute(check_sql)
    result = cur.fetchone()
    if result:
        return -2
    
    # チャネルIDを挿入
    insert_sql = f"insert ignore into channel_ids (id, guild_id) values ({str(channel.id)}, {str(channel.guild.id)});"
    try:
        cur.execute(insert_sql)
        conn.commit()
    except Exception as e:
        print(e)
        return -4

    cur.close()
    conn.close()
    
    return 1

async def get_log_channels(guild_id: int) -> list[int]:
    # DBへ接続
    conn = mysql.connector.connect(
        user=Var.MYSQL_USER,
        password=Var.MYSQL_PASSWORD,
        host=Var.MYSQL_HOST,
        port=Var.MYSQL_PORT,
        database=Var.MYSQL_DB
    )
    
    # DBの接続確認
    if not conn.is_connected():
        return []
    
    try:
        cur = conn.cursor()
        
        # チャネルIDを取得
        select_sql = f"select id from channel_ids where guild_id = {str(guild_id)};"
        cur.execute(select_sql)
        result = []
        for result_line in cur.fetchall():
            result.append(result_line[0])
        
        print(result)
        
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        return []
    
    return result

async def send_log_channel(content: str, channel_list: list[int], guild: discord.Guild, embed: discord.Embed = None, embeds: list[discord.Embed] = None) -> int:
    channel: discord.abc.GuildChannel
    if embeds == None and embed != None:
        embeds = [embed]
    if embeds == None and embed == None:
        return -1
    for channel_id in channel_list:
        channel = guild.get_channel(channel_id)
        if channel == None:
            continue
        await channel.send(content=content, embeds=embeds)
    return 1