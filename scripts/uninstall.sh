#!/bin/sh

# Include config variables
. "$PWD"/config


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
PREFERENCES_DIR=$(expand_home "$PREFERENCES_DIR")
APP_ICON_FILE=$(expand_home "$APP_ICON_FILE")

rm -rfv "$BIN_FILE" \
        "$PYTHON_PKG_DIR" \
        "$APP_ICON_FILE" \
        "$DATA_DIR" \
        "$DESKTOP_FILE" \
        "$DB_DIR" \
        "$PREFERENCES_DIR"
