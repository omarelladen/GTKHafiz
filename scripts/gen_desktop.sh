#!/bin/sh

# Include config variables
. "$PWD"/config


echo "[Desktop Entry]
Name=$APP_NAME
Comment=$APP_DESCRIPTION
Exec=$BIN_FILE
Type=Application
Categories=Education
Icon=$APP_NAME_LOWER" > "$ORIG_DESKTOP_FILE"
