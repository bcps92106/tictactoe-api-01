#!/bin/bash
# 自動更新 Git 的腳本
# 用法： ./update.sh "修改訊息"
if [ -z "$1" ]; then
  echo "❌ 請輸入提交訊息，例如： ./update.sh '修正棋盤邏輯'"
  exit 1
fi
git add .
git commit -m "$1"
git push origin main