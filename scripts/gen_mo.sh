#!/bin/sh

# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

# Include config variables
. "$PWD"/configs


while read -r lang || [ -n "$lang" ]; do
    case "$lang" in ''|'#'*) continue ;; esac

    in_file="$PO_DIR/$lang.po"
    out_dir="$LOCALE_DIR/$lang/LC_MESSAGES"

    if [ -f "$in_file" ]; then
        mkdir -vp "$out_dir"
        msgfmt -v "$in_file" -o "$out_dir/$EXE_NAME.mo"
    fi
done < "$PO_DIR/LINGUAS"
