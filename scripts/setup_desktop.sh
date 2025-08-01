#!/bin/sh

root_dir=${1:-$HOME}


echo "[Desktop Entry]
Name=GTK Hafiz
Comment=Track Qur'an memorization visually
Exec=sh $root_dir/GTK-Hafiz/scripts/launcher.sh
Type=Application
Icon=$root_dir/GTK-Hafiz/imgs/icon.png" > "$HOME"/.local/share/applications/gtk-hafiz.desktop


echo "#!/bin/sh

cd "$root_dir"/GTK-Hafiz && /usr/bin/python3 src/main.py" > "$PWD"/scripts/launcher.sh
