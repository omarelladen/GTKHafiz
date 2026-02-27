#!/bin/sh

# Include config variables
. "$PWD"/config
. "$PWD"/scripts/expand_home.sh

SUDO=
SUDO_U=
if command -v sudo >/dev/null 2>&1 \
   && [ "$(id -u 2>/dev/null)" = "0" ] \
   && [ -n "$SUDO_USER" ]; then
    SUDO=sudo
    SUDO_U="sudo -u $SUDO_USER"
fi

scripts/uninstall.sh

ICON_FILE=$(expand_home "$ICON_FILE")

BIN_DIR=$(dirname "$BIN_FILE")
MAN_DIR=$(dirname "$MAN_FILE")
ICON_DIR=$(dirname "$ICON_FILE")
DESKTOP_DIR=$(dirname "$DESKTOP_FILE")

mkdir -pv "$BIN_DIR" \
          "$MAN_DIR" \
          "$DATA_DIR" \
          "$ICON_DIR" \
          "$PYTHON_PKG_DIR" \
          "$DESKTOP_DIR"

cp -v "$ORIG_SRC_DIR"/* "$PYTHON_PKG_DIR"
cp -v "$ORIG_ICON_FILE" "$ICON_FILE"
cp -v config "$DATA_DIR"
cp -v "$ORIG_DB_SCRIPT" "$DB_SCRIPT"
cp -v "$ORIG_BAR_SIZES_FILE" "$DATA_DIR"
cp -v "$ORIG_BOOKS_FILE" "$BOOKS_FILE"
cp -v "$ORIG_CHAPTERS_FILE" "$CHAPTERS_FILE"
cp -v "$ORIG_DESKTOP_FILE" "$DESKTOP_FILE"
cp -v "$ORIG_BIN_FILE" "$BIN_FILE"
cp -v "$ORIG_MAN_FILE" "$MAN_FILE"

chmod -v +x "$BIN_FILE"
