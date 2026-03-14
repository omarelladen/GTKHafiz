#!/bin/sh

# Copyright 2025-2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

files_rm=files.txt

sed -i 's|^usr/|/usr/|' "$files_rm"
xargs rm -vrf < "$files_rm"
