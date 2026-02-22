import os


class PreferencesManager():
    def __init__(self,
        preferences_path
    ):
        self.preferences_path = os.path.expanduser(preferences_path)

    def read_rect_color_from_file(self):
        if os.path.isfile(self.preferences_path):
            try:
                preferences = {}
                with open(self.preferences_path, 'r') as f:
                    exec(f.read(), preferences)

                RECT_COLOR = preferences.get("RECT_COLOR")
                if RECT_COLOR:
                    return RECT_COLOR.strip()
            except Exception as e:
                print("Failed to load preferences "
                     f"from '{self.preferences_path}': {e}"
                )
                return None
        return None

    def write_rect_color_to_file(self, color_hex):
        try:
            dir_path = os.path.dirname(self.preferences_path)
            os.makedirs(dir_path, exist_ok=True)
            with open(self.preferences_path, 'w') as f:
                f.write(f'RECT_COLOR="{color_hex}"\n')
        except Exception as e:
            print("Failed to write preferences "
                 f"at '{self.preferences_path}': {e}"
            )
