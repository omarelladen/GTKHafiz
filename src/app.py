import os
import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .db_manager import DBManager
from .preferences_manager import PreferencesManager
from .window import Window


class App():
    def __init__(self):
        self.args = sys.argv[1:]

        # Config variables
        self.configs = {}
        with open("/usr/local/share/gtkhafiz/config", "r") as f:
            exec(f.read(), self.configs)

        # Metadata
        self.name          = self.configs.get("APP_NAME")
        self.name_lower    = self.configs.get("APP_NAME_LOWER")
        self.description   = self.configs.get("APP_DESCRIPTION")
        self.version       = self.configs.get("APP_VERSION")
        self.website_url   = self.configs.get("WEBSITE_URL")
        self.website_label = self.configs.get("WEBSITE_LABEL")
        self.authors       = self.configs.get("AUTHORS").split(",")
        self.copyright     = self.configs.get("COPYRIGHT")

        self.db_manager = None
        self.user = None
        self.win = None
        self.user_data_changed = None

    def setup(self):
        # DB Manager
        self.db_manager = DBManager(
            os.path.expanduser(self.configs.get("DB_FILE")),
            self.configs.get("DB_SCRIPT")
        )
        self.user = self.db_manager.load_user()
        book = self.db_manager.load_book()
        book.list_chapters = self.db_manager.load_chapters()

        # Preferences Manager
        preferences_manager = PreferencesManager(
            os.path.expanduser(self.configs.get("PREFERENCES_FILE"))
        )

        # Flag to save data or not on db when the app is closed
        self.user_data_changed = False

        # Window
        self.win = Window(
            self,
            self.user,
            book,
            preferences_manager,
            self.configs.get("BAR_SIZES_FILE"),
            self.configs.get("APP_ICON_FILE")
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
        print(
            "Usage:\n"
           f"  {self.name_lower} [OPTION…]\n"
            "\n"
            "Help Options:\n"
            "  -h, --help                 Show help options\n"
            "\n"
            "Application Options:\n"
            "  -v, --version              Print version information and exit\n"
        )

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
