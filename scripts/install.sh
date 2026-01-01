#!/bin/sh

# Include config variables
. "$PWD"/config


SUDO=
SUDO_U=

if command -v sudo >/dev/null 2>&1 \
   && [ "$(id -u 2>/dev/null)" = "0" ] \
   && [ -n "$SUDO_USER" ]; then
    SUDO=sudo
    SUDO_U="sudo -u $SUDO_USER"
fi

echo "USER=$USER"
echo "SUDO=$SUDO"
echo "SUDO_U=$SUDO_U"
echo "SUDO_USER=$SUDO_USER"

scripts/uninstall.sh

expand_home()
{
	_PATH="$1"

	case "$_PATH" in
		"~"|"~"/*)
			_PATH="/home/${SUDO_USER:-$USER}${_PATH#\~}" ;;
	esac

	echo "$_PATH"
}

DB_DIR=$(expand_home "$DB_DIR")
DB_FILE=$(expand_home "$DB_FILE")
PREFERENCES_DIR=$(expand_home "$PREFERENCES_DIR")
PREFERENCES_FILE=$(expand_home "$PREFERENCES_FILE")

mkdir -pv "$BIN_DIR" "$DATA_DIR" "$ICONS_DIR" "$PYTHON_PKG_DIR" "$DESKTOP_DIR"
eval "$SUDO_U mkdir -pv \"$DB_DIR\" \"$PREFERENCES_DIR\""

cp -v "$ORIG_SRC_DIR"/* "$PYTHON_PKG_DIR"
cp -v "$ORIG_ICONS_DIR"/* "$ICONS_DIR"
cp -v config "$DATA_DIR"
eval "$SUDO_U cp -v \"$ORIG_DB_FILE\" \"$DB_FILE\""
cp -v "$ORIG_BAR_SIZES_FILE" "$DATA_DIR"
eval "$SUDO_U cp -v \"$ORIG_PREFERENCES_FILE\" \"$PREFERENCES_FILE\""

echo "# This directory is a Python package." > "$PYTHON_PKG_DIR"/__init__.py


echo "[Desktop Entry]
Name=$APP_NAME
Comment=$APP_DESCRIPTION
Exec=$BIN_FILE
Type=Application
Categories=Education
Icon=$APP_ICON_FILE" > "$DESKTOP_FILE"


echo "#!/usr/bin/python3

import sys
sys.path.insert(0, \"$DATA_DIR\")

from $APP_NAME_LOWER.main import main

if __name__ == \"__main__\":
    main()
" > "$BIN_FILE"

chmod -v +x "$BIN_FILE"
