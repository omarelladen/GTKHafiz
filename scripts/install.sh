#!/bin/sh

# Include config variables
. "$PWD"/config


./scripts/uninstall.sh


mkdir -pv "$BIN_DIR" "$DATA_DIR" "$ICONS_DIR" "$PYTHON_PKG_DIR" "$DESKTOP_DIR" "/home/$SUDO_USER/$DB_DIR"

cp -v "$ORIG_SRC_DIR"/* "$PYTHON_PKG_DIR"
cp -v "$ORIG_ICONS_DIR"/* "$ICONS_DIR"
cp -v config "$DATA_DIR"
cp -v "$ORIG_DB_FILE" "/home/$SUDO_USER/$DB_FILE"
cp -v "$ORIG_BAR_SIZES_FILE" "$DATA_DIR"

chmod -v a+wx  "/home/$SUDO_USER/$DB_DIR"
chmod -v a+wx "/home/$SUDO_USER/$DB_FILE"

echo "# This directory is a Python package." > "$PYTHON_PKG_DIR"/__init__.py


echo "[Desktop Entry]
Name=$APP_NAME
Comment=$APP_DESCRIPTION
Exec=$BIN_FILE
Type=Application
Icon=$APP_ICON_FILE" > "$DESKTOP_FILE"


echo "#!/usr/bin/python3

import sys
sys.path.insert(0, \"$DATA_DIR\")

from $APP_NAME_LOWER.main import main

if __name__ == '__main__':
    main()
" > "$BIN_FILE"

chmod -v a+x "$BIN_FILE"
