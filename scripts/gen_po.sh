#!/bin/sh

# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

# Include config variables
. "$PWD"/configs


pot_file="$PO_DIR/$EXE_NAME.pot"
potfiles_file="$PO_DIR/POTFILES"
linguas_file="$PO_DIR/LINGUAS"

mkdir -vp "$PO_DIR"


ls src/*.py > "$potfiles_file"
xgettext --from-code=UTF-8 -f "$potfiles_file" -o "$pot_file"


if [ -f "$linguas_file" ]; then
    while read -r lang || [ -n "$lang" ]; do
        case "$lang" in ''|'#'*) continue ;; esac

        po_file="$PO_DIR/$lang.po"

        if [ -f "$po_file" ]; then
            msgmerge -v --update "$po_file" "$pot_file"
        else
            msginit -i "$pot_file" -l "$lang" -o "$po_file" --no-translator
        fi
    done < "$linguas_file"
fi
