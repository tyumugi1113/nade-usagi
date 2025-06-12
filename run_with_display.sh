#!/bin/bash

# WSL環境でPyGameを実行するためのスクリプト
# X11サーバーへの接続を設定し、ゲームを起動します

# DISPLAYが設定されていない場合はデフォルト値を設定
if [ -z "$DISPLAY" ]; then
    export DISPLAY=:0
fi

# フォントキャッシュを更新
fc-cache -f -v

# 利用可能なフォントを表示（デバッグ用）
echo "Available fonts:"
fc-list | grep -i ipa
fc-list | grep -i noto
fc-list | grep -i gothic

# ゲームを実行
python3 run.py
