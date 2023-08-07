#!/bin/env bash

# Chats
telegram-desktop &
chromium --app=https://teams.microsoft.com &

# Display
~/bin/wallpaper.sh &
redshift -t 5500:2500 -l 50:14 &
~/bin/dualscreen_left &
unclutter -grab -idle 1 -root &
dunst &

# Tools
udiskie &

# Music
spotblock &
spotify &

# Keyboard bindings
[[ -f ~/.Xmodmap ]] && xmodmap ~/.Xmodmap
