#!/bin/sh

po_dir=po
pot_file="$po_dir"/gtkhafiz.pot
lang=pt_BR

mkdir -p "$po_dir"

xgettext --from-code=UTF-8 src/*.py -o "$pot_file"

msginit -i "$pot_file" -l "$lang" -o "$po_dir"/"$lang".po
