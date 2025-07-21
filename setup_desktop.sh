#!/bin/sh

echo "[Desktop Entry]
Name=GTK Hafiz
Comment=Track Qur'an memorization visually
Exec=sh $HOME/GTK-Hafiz/launcher.sh
Type=Application
Icon=$HOME/GTK-Hafiz/imgs/icon.png" > "$HOME"/.local/share/applications/gtk-hafiz.desktop
