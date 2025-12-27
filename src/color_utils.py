import re

from gi.repository import  Gdk

class ColorUtils():
    def __init__(self):
        pass

    def is_valid_color_hex(self, color_hex):
        _color_hex = color_hex.strip().lstrip("#").lower()
        if re.fullmatch(r"[0-9a-f]{6}|[0-9a-f]{8}", _color_hex):
            return True
        return False

    def rgba_to_hex(self, color_rgba):
        r = int(color_rgba.red   * 255)
        g = int(color_rgba.green * 255)
        b = int(color_rgba.blue  * 255)
        a = int(color_rgba.alpha * 255)
        return f"#{r:02X}{g:02X}{b:02X}{a:02X}"

    def hex_to_rgba(self, color_hex):
        _color_hex = color_hex.lstrip('#')

        r = int(_color_hex[0:2], 16) / 255.0
        g = int(_color_hex[2:4], 16) / 255.0
        b = int(_color_hex[4:6], 16) / 255.0
        a = int(_color_hex[6:8], 16) / 255.0 if len(color_hex) == 8 else 1.0

        return Gdk.RGBA(r, g, b, a)
