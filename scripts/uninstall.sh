#!/bin/sh

# Include config variables
. "$PWD"/config


rm -rfv "$BIN_FILE" "$PYTHON_PKG_DIR" "ICONS_DIR" "$DATA_DIR" "$DESKTOP_FILE"  "/home/$SUDO_USER/$DB_DIR"
