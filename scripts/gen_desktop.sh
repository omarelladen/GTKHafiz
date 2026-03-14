#!/bin/sh

# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

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
