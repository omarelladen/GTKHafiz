import gi
from gi.repository import Gdk

class Rectangle(Gdk.Rectangle):
    def __init__(self,
        x,
        y,
        width,
        height,
        caption = None,
        color_off: tuple[float, float, float] = (0.5, 0.5, 0.5),
        color_on: tuple[float, float, float] = (0.0, 0.8, 0.0),
        color: tuple[float, float, float] = (0.0, 0.8, 0.0)
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.caption = caption
        self.color_off = color_off
        self.color_on = color_on
        self.color = color
