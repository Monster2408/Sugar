#!/bin/bash
#
# minecraft_server start/stop/status script
# サーバーを複数起動する場合はjarファイルの名前を「spigot-1.12.2-1.jar」に変更して「SERVICE」の中身も同じように変更する必要性有
#

## Minecraft用設定
# mincraft_server.jar 実行ユーザ
USERNAME='monster2408'

# session名
SESSION_NAME='sugar-bot'

# minecraft_serverディレクトリ
MC_PATH='/home/monster2408/python/sugar/'

# 実行するminecraft_server.jar
SERVICE='main.py'

## 制御システム
cd $MC_PATH

ME=`whoami`

if [ $ME != $USERNAME ]; then
  echo "Please run the $USERNAME user."
  exit
fi

## コマンド部分
# bot 開始処理
start() {
  if pgrep -u $USERNAME -f $SERVICE > /dev/null; then
    echo "$SERVICE is already running!"
  else
    echo "Starting $SERVICE..."
    tmux new-session -d -s $SESSION_NAME
    tmux send-keys -t $SESSION_NAME:0 "cd $MC_PATH" C-m
    tmux send-keys -t $SESSION_NAME:0 "python3 $SERVICE" C-m
  fi
  exit
}

# bot 停止処理
stop() {
  if pgrep -u $USERNAME -f $SERVICE > /dev/null; then
		tmux send-keys -t $SESSION_NAME:0 "" C-c
		sleep 5
    tmux kill-session -t $SESSION_NAME
		echo "Stoped $SERVICE"
  else
    echo "$SERVICE is not running!"
  fi
	exit
}

# Minecraft 再起動処理
restart() {
  if pgrep -u $USERNAME -f $SERVICE > /dev/null; then
		tmux send-keys -t $SESSION_NAME:0 "" C-c
		sleep 5
    tmux kill-session -t $SESSION_NAME
		echo "Stoped $SERVICE"
  else
    echo "$SERVICE is not running!"
  fi
  start
  exit
}

# Minecraft 起動状態確認処理
status() {
  if pgrep -u $USERNAME -f $SERVICE > /dev/null; then
    echo "$SERVICE is already running!"
  else
    echo "$SERVICE is not running!"
  fi
  exit
}

# pip install
pip_install() {
  if pgrep -u $USERNAME -f $SERVICE > /dev/null; then
		tmux send-keys -t $SESSION_NAME:0 "" C-c
		sleep 5
    tmux kill-session -t $SESSION_NAME
		echo "Stoped $SERVICE"
  fi
  python3 -m pip install -r requirements.txt
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    restart
    ;;
  status)
    status
    ;;
  pip_install)
    pip_install
    ;;
  *)
    echo  $"Usage: $0 {start|stop|restart|status|pip_install}"
esac 