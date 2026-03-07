#!/bin/sh

# Include config variables
. "$PWD"/configs

. "$PWD"/scripts/expand_home.sh


RM_FILES=files.txt
DB_FILE=$(expand_home "$DB_FILE")
PREFERENCES_FILE=$(expand_home "$PREFERENCES_FILE")

sed -i 's|^usr/|/usr/|' "$RM_FILES"
xargs rm -vrf < "$RM_FILES"
rm -vf "$DB_FILE" "$PREFERENCES_FILE"
