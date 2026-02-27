#!/bin/sh

# Include config variables
. "$PWD"/config
. "$PWD"/scripts/expand_home.sh

DB_FILE=$(expand_home "$DB_FILE")
PREFERENCES_FILE=$(expand_home "$PREFERENCES_FILE")
ICON_FILE=$(expand_home "$ICON_FILE")

DB_DIR=$(dirname "$DB_FILE")
PREFERENCES_DIR=$(dirname "$PREFERENCES_FILE")

rm -rfv "$BIN_FILE" \
        "$MAN_FILE" \
        "$PYTHON_PKG_DIR" \
        "$ICON_FILE" \
        "$DATA_DIR" \
        "$DESKTOP_FILE" \
        "$DB_DIR" \
        "$PREFERENCES_DIR"
