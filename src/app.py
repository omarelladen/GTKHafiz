# Copyright 2025-2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .db_manager import DBManager
from .preferences_manager import PreferencesManager
from .window import Window


class App():
    def __init__(self, exe_name, prefix, configs):
        self.prefix = prefix
        self.exe_name = exe_name

        # Metadata
        self.configs = configs
        self.name          = self.configs.get("APP_NAME")
        self.description   = self.configs.get("APP_DESCRIPTION")
        self.version       = self.configs.get("APP_VERSION")
        self.website_url   = self.configs.get("WEBSITE_URL")
        self.website_label = self.configs.get("WEBSITE_LABEL")
        self.authors       = [self.configs.get("AUTHOR")]
        self.copyright     = self.configs.get("COPYRIGHT")

        self.db_manager = None
        self.user = None
        self.win = None
        self.user_data_changed = None

    def setup(self):
        # DB Manager
        self.db_manager = DBManager(
            db_path=os.path.join(
                os.path.expanduser(self.configs.get("DB_DIR")),
                self.exe_name,
                self.configs.get("DB_FILENAME")
            ),
            db_script_path=os.path.join(
                self.prefix,
                self.configs.get("DATA_DIR"),
                self.exe_name,
                self.configs.get("DB_SCRIPT")
            )
        )
        self.user = self.db_manager.load_user()
        book = self.db_manager.load_book()
        book.list_chapters = self.db_manager.load_chapters()

        # Preferences Manager
        preferences_manager = PreferencesManager(
            preferences_path=os.path.join(
                os.path.expanduser(self.configs.get("PREFERENCES_DIR")),
                self.exe_name,
                self.configs.get("PREFERENCES_FILENAME")
            )
        )

        # Flag to save data or not on db when the app is closed
        self.user_data_changed = False


        if not Gtk.init_check()[0]:
            print(_("Failed to start GUI: cannot open display"))
            return False

        # Window
        self.win = Window(
            app=self,
            user=self.user,
            book=book,
            preferences_manager=preferences_manager,
            bars_sizes_path=os.path.join(
                self.prefix,
                self.configs.get("DATA_DIR"),
                self.exe_name,
                self.configs.get("BAR_SIZES_FILENAME")
            ),
            app_icon_path=os.path.join(
                self.prefix,
                self.configs.get("ICON_DIR"),
                self.exe_name + "." + self.configs.get("ICON_EXT")
            )
        )
        self.win.connect("destroy", self._on_destroy)
        self.win.show_all()

        return True

    def _on_destroy(self, window):
        self.quit()

    def quit(self):
        if self.user_data_changed:
            self.db_manager.save_user_data(self.user)
        Gtk.main_quit()

    def run(self):
        Gtk.main()
