import os
import csv
import gi

from gi.repository import Gdk

class PreferencesManager():
    def __init__(self,
        preferences_path = None,
    ):
        self.preferences_path = os.path.expanduser(preferences_path)

        self.preferences = {}
        with open(self.preferences_path, 'r') as f:
            exec(f.read(), self.preferences)        

    def read_rect_color_from_file(self):
        if os.path.isfile(self.preferences_path):
            try:
                
                RECT_COLOR = self.preferences.get("RECT_COLOR")
                if RECT_COLOR:
                    return RECT_COLOR.strip()
            except Exception as e:
                print(f'Failed to load preferences from "{self.preferences_path}": {e}')
                return None
        return None

    def write_rect_color_to_file(self, color_hex):
        try:
            with open(self.preferences_path, 'w') as f:
                f.write(f'RECT_COLOR="{color_hex}"')
        except Exception as e:
            print(f'Failed to write preferences at "{self.preferences_path}": {e}')
