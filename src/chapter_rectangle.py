import gi
from gi.repository import Gdk

class ChapterRectangle(Gdk.Rectangle):
    def __init__(self,
        x,
        y,
        width,
        height,
        caption = None,
        color_on:  tuple[float, float, float] = (0.0, 0.8, 0.0),
        color_off: tuple[float, float, float] = (0.5, 0.5, 0.5),
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.caption = caption
        self.color_off = color_off
        self.color_on = color_on
        self.color = color_off

    def paint_on(self):
        self.color = self.color_on

    def paint_off(self):
        self.color = self.color_off
