#!/bin/sh

files_rm=files.txt

sed -i 's|^usr/|/usr/|' "$files_rm"
xargs rm -vrf < "$files_rm"
