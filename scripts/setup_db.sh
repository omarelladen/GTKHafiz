#!/bin/sh

# Copyright 2025-2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

# Include config variables
. "$PWD"/configs


db_file="$1"

sqlite3 "$db_file" <<EOF
CREATE TABLE IF NOT EXISTS
books
(
    id          INTEGER PRIMARY KEY,
    name_arabic TEXT DEFAULT '',
    name_latin  TEXT DEFAULT '',
    n_chapters  INTEGER DEFAULT 0,
    n_verses    INTEGER DEFAULT 0,
    n_words     INTEGER DEFAULT 0,
    n_letters   INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS
chapters
(
    number      INTEGER PRIMARY KEY,
    name_arabic TEXT DEFAULT '',
    name_latin  TEXT DEFAULT '',
    n_verses    INTEGER DEFAULT 0,
    n_words     INTEGER DEFAULT 0,
    n_letters   INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS
users
(
    username       TEXT PRIMARY KEY,
    n_mem_chapters INTEGER DEFAULT 0,
    n_mem_words    INTEGER DEFAULT 0,
    n_mem_verses   INTEGER DEFAULT 0,
    n_mem_letters  INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS
mem_chapters
(
    users_username  INTEGER REFERENCES users(username),
    chapters_number INTEGER REFERENCES chapters(number)
);

.mode csv
.import "$BOOKS_FILE" books
.import "$CHAPTERS_FILE" chapters

EOF
