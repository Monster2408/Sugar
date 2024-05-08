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
                id bigint(20) not null auto_increment primary key
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
    insert_sql = f"insert ignore into channel_ids (id) values ({str(channel.id)});"
    try:
        cur.execute(insert_sql)
        conn.commit()
    except Exception as e:
        print(e)
        return -4

    cur.close()
    conn.close()
    
    return 1



RESPONSE_DICT: dict[str, str] = {
    "failed_to_connect_db": "データベースに接続できませんでした。",
}