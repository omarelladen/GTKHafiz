#!/bin/sh

PO_DIR=po
POT_FILE="$PO_DIR"/gtkhafiz.pot

mkdir -p "$PO_DIR"

xgettext --from-code=UTF-8 src/*.py -o "$POT_FILE"

msginit -i "$POT_FILE" -l pt_BR -o "$PO_DIR"/pt_BR.po
