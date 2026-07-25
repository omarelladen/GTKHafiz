#!/bin/sh

# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

# Include config variables
. "$PWD"/configs


desktop_file="$ORIG_DESKTOP_DIR/$EXE_NAME.desktop"

echo "[Desktop Entry]
Name=$APP_NAME
Comment=$DESCRIPTION
Exec=$EXE_NAME
Type=Application
Categories=$CATEGORIES
Keywords=$KEYWORDS
Icon=$EXE_NAME" > "$desktop_file"
