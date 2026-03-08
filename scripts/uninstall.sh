#!/bin/sh

RM_FILES=files.txt

sed -i 's|^usr/|/usr/|' "$RM_FILES"
xargs rm -vrf < "$RM_FILES"
