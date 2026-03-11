#!/bin/sh

# Include config variables
. "$PWD"/configs

mkdir -vp "$PO_DIR"


ls src/*.py > "$POTFILES_FILE"
xgettext --from-code=UTF-8 -f "$POTFILES_FILE" -o "$POT_FILE"


if [ -f "$LINGUAS_FILE" ]; then
    while read -r lang || [ -n "$lang" ]; do
        case "$lang" in ''|'#'*) continue ;; esac

        po_file="$PO_DIR/$lang.po"

        if [ -f "$po_file" ]; then
            msgmerge -v --update "$po_file" "$POT_FILE"
        else
            msginit -i "$POT_FILE" -l "$lang" -o "$po_file" --no-translator
        fi
    done < "$LINGUAS_FILE"
fi
