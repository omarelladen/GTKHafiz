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

scripts/uninstall.sh

expand_home()
{
    _PATH="$1"

    case "$_PATH" in
        "~"|"~"/*)
            USER_NAME=$(whoami)
            _PATH="/home/${SUDO_USER:-$USER_NAME}${_PATH#\~}" ;;
    esac

    echo "$_PATH"
}

DB_DIR=$(expand_home "$DB_DIR")
DB_FILE=$(expand_home "$DB_FILE")

mkdir -pv "$BIN_DIR" "$DATA_DIR" "$ICONS_DIR" "$PYTHON_PKG_DIR" "$DESKTOP_DIR"
eval "$SUDO_U mkdir -pv \"$DB_DIR\""

cp -v "$ORIG_SRC_DIR"/* "$PYTHON_PKG_DIR"
cp -v "$ORIG_ICONS_DIR"/* "$ICONS_DIR"
cp -v config "$DATA_DIR"
eval "$SUDO_U cp -v \"$ORIG_DB_FILE\" \"$DB_FILE\""
cp -v "$ORIG_BAR_SIZES_FILE" "$DATA_DIR"
cp -v "$ORIG_DESKTOP_FILE" "$DESKTOP_FILE"
cp -v "$ORIG_BIN_FILE" "$BIN_FILE"

chmod -v +x "$BIN_FILE"
