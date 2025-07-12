#!/bin/bash

DB="db.sqlite3"

if [ -f "$DB" ]; then
    rm "$DB"
fi

sqlite3 "$DB" <<EOF

CREATE TABLE IF NOT EXISTS
books(
    id          INTEGER PRIMARY KEY,
    name_arabic TEXT DEFAULT '',
    name_latin  TEXT DEFAULT '',
    n_chapters  INTEGER DEFAULT 0,
    n_verses    INTEGER DEFAULT 0,
    n_words     INTEGER DEFAULT 0,
    n_letters   INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS
chapters(
    number      INTEGER PRIMARY KEY,
    name_arabic TEXT DEFAULT '',
    name_latin  TEXT DEFAULT '',
    n_verses    INTEGER DEFAULT 0,
    n_words     INTEGER DEFAULT 0,
    n_letters   INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS
users(
    username       TEXT PRIMARY KEY,
    full_name      TEXT DEFAULT '',
    country        TEXT DEFAULT '',
    n_mem_chapters INTEGER DEFAULT 0,
    n_mem_words    INTEGER DEFAULT 0,
    n_mem_verses   INTEGER DEFAULT 0,
    n_mem_letters  INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS
mem_chapters(
    users_username  INTEGER REFERENCES users(username),
    chapters_number INTEGER REFERENCES chapters(number)
);

CREATE TABLE IF NOT EXISTS
parts(
    number        INTEGER PRIMARY KEY,
    start_chapter INTEGER DEFAULT 0,
    start_verse   INTEGER DEFAULT 0,
    end_chapter   INTEGER DEFAULT 0,
    end_verse     INTEGER DEFAULT 0
);

.mode csv

.import csv/books.csv books
.import csv/chapters.csv chapters
#.import csv/users.csv users
.import csv/parts.csv parts

EOF
