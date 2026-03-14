# Copyright 2025-2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

class Book:
    def __init__(
        self,
        name_arabic,
        name_latin,
        n_chapters,
        n_verses,
        n_words,
        n_letters,
        list_chapters=None,
    ):
        self.name_arabic = name_arabic
        self.name_latin = name_latin
        self.n_chapters = n_chapters
        self.n_verses = n_verses
        self.n_words = n_words
        self.n_letters = n_letters
        self.list_chapters = list_chapters if list_chapters else []
