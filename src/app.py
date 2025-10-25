import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .db_manager import DBManager
from .window import Window

# Include config variables
exec(open("/usr/local/share/gtkhafiz/config").read())

class App():
    def __init__(self):
        self.db_manager = DBManager(os.path.expanduser(DB_FILE))
        
        # Load persistant data from db
        self.user = self.db_manager.load_user()
        self.book = self.db_manager.load_book()
        self.book.list_chapters = self.db_manager.load_chapters()

        # Flag to save data or not on db when the app is closed
        self.user_data_changed = False

        # Load GTK Window
        self.win = Window(self,
                         BAR_SIZES_FILE,
                         APP_NAME,
                         APP_DESCRIPTION,
                         APP_VERSION,
                         WEBSITE_URL,
                         WEBSITE_LABEL,
                         AUTHORS,
                         COPYRIGHT,
                         APP_ICON_FILE,
                         MENU_ICON,
                         SAVE_ICON
        )
        self.win.connect("destroy", self._on_destroy)
        self.win.show_all()
    
    def _on_destroy(self, window):
        self.quit()

    def quit(self):
        if self.user_data_changed:
            self.db_manager.save_user_data(self.user)
        Gtk.main_quit()
        
    def run(self):
        Gtk.main()
