# Copyright 2025-2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

from gi.repository import Gdk


class ChapterRectangle(Gdk.Rectangle):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        juz,
        chapter,
        color_on: Gdk.RGBA,
        color_off=Gdk.RGBA(0.5, 0.5, 0.5, 1.0),
    ):
        self.og_x = x
        self.og_y = y
        self.og_width = width
        self.og_height = height

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.juz = juz
        self.chapter = chapter

        self.color_off = color_off
        self.color_on = color_on
        self.color = color_off

    def paint_on(self):
        self.color = self.color_on

    def paint_off(self):
        self.color = self.color_off
