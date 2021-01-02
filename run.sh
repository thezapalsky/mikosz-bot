#!/bin/bash
echo "siema eniu -- odpalam bota"
pkill -f mikosz
cd ~/Projects/mikosz-bot
nohup python3 -u /Users/mikolaj/Projects/mikosz-bot/mikosz-bot.py &
nohup python3 -u /Users/mikolaj/Projects/mikosz-bot/mikosz-bot-fb.py &
echo "done"