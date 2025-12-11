import os
import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .window import Window
from .db_manager import DBManager
from .preferences_manager import PreferencesManager

# Include config variables
exec(open("/usr/local/share/gtkhafiz/config").read())

class App():
    def __init__(self):
        self.args = sys.argv[1:]

        # Metadata
        self.name = APP_NAME
        self.name_lower = APP_NAME_LOWER
        self.description = APP_DESCRIPTION
        self.version = APP_VERSION
        self.website_url = WEBSITE_URL
        self.website_label = WEBSITE_LABEL
        self.authors = AUTHORS.split(",")
        self.copyright = COPYRIGHT

        self.db_manager = DBManager(os.path.expanduser(DB_FILE))

        # Load persistant data from db
        self.user = self.db_manager.load_user()
        self.book = self.db_manager.load_book()
        self.book.list_chapters = self.db_manager.load_chapters()

        # Flag to save data or not on db when the app is closed
        self.user_data_changed = False

        # Preferences Manager
        self.preferences_manager = PreferencesManager(os.path.expanduser(PREFERENCES_FILE))

        # Load GTK Window
        self.win = Window(
            self,
            BAR_SIZES_FILE,
            APP_ICON_FILE
        )
        self.win.connect("destroy", self._on_destroy)
        self.win.show_all()

    def parse_args(self):
        if "--help" in self.args or "-h" in self.args:
            self.show_help()
            sys.exit(0)
        elif "--version" in self.args or "-v" in self.args:
            self.show_version()
            sys.exit(0)

    def show_help(self):
        print("Usage:")
        print(f"  {self.name_lower} [OPTION…]")
        print("")
        print("Help Options:")
        print("  -h, --help                 Show help options")
        print("")
        print("Application Options:")
        print("  -v, --version              Print version information and exit")

    def show_version(self):
        print(f"{self.name} {self.version}")

    def _on_destroy(self, window):
        self.quit()

    def quit(self):
        if self.user_data_changed:
            self.db_manager.save_user_data(self.user)
        Gtk.main_quit()

    def run(self):
        Gtk.main()
