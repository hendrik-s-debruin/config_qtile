#!/bin/env bash

# Chats
telegram-desktop &
signal-desktop &
slack &

# Display
~/bin/wallpaper.sh &
redshift -t 5500:2500 -l 50:14 &
~/bin/dualscreen_left &
unclutter -grab -idle 1 -root &
dunst &

# Tools
udiskie &
fcitx &
xmod ~/.Xmodmap &

# Music
spotblock &
spotify &
