#!/bin/sh

# Include config variables
. "$PWD"/configs


echo "[Desktop Entry]
Name=$APP_NAME
Comment=$APP_DESCRIPTION
Exec=$APP_NAME_LOWER
Type=Application
Categories=Education;GTK
Keywords=$KEYWORDS
Icon=$APP_NAME_LOWER" > "$ORIG_DESKTOP_FILE"
