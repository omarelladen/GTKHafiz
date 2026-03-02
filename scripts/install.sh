#!/bin/sh

CONFIG_FILENAME=config

# Include config variables
. ./"$CONFIG_FILENAME"
. ./scripts/expand_home.sh

scripts/uninstall.sh


OWNER="${SUDO_USER:-$(whoami)}"

ICON_FILE=$(expand_home "$ICON_FILE")

# Executables (rwxr-xr-x)
install -vD -m 755 "$ORIG_BIN_FILE" "$BIN_FILE"
install -vD -m 755 "$ORIG_DB_SCRIPT" "$DB_SCRIPT"

# Normal files (rw-r--r--)

mkdir -vp "$PYTHON_PKG_DIR"
install -v -m 644 "$ORIG_SRC_DIR"/* "$PYTHON_PKG_DIR"

install -vD -m 644 -o "$OWNER" "$ORIG_ICON_FILE" "$ICON_FILE"
install -vD -m 644 "$CONFIG_FILENAME" "$DATA_DIR/$CONFIG_FILENAME"
install -vD -m 644 "$ORIG_BAR_SIZES_FILE" "$BAR_SIZES_FILE"
install -vD -m 644 "$ORIG_BOOKS_FILE" "$BOOKS_FILE"
install -vD -m 644 "$ORIG_CHAPTERS_FILE" "$CHAPTERS_FILE"
install -vD -m 644 "$ORIG_DESKTOP_FILE" "$DESKTOP_FILE"
install -vD -m 644 "$ORIG_MAN_FILE" "$MAN_FILE"
