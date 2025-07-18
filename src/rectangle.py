import gi
from gi.repository import Gdk

class Rectangle(Gdk.Rectangle):
    def __init__(self,
        x         :int = 0,
        y         :int = 0,
        width     :int = 0,
        height    :int = 0,
        caption   :int = 0,
        off_color :tuple[float, float, float] = (0.5, 0.5, 0.5),
        on_color  :tuple[float, float, float] = (0.0, 0.8, 0.0),
        color     :tuple[float, float, float] = (0.0, 0.8, 0.0)
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.caption = caption
        self.off_color = off_color
        self.on_color = on_color
        self.color = color
