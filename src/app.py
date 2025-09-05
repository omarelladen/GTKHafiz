import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from db_manager import DBManager
from window import Window

# Include config variables
exec(open('config').read())

class App():
    def __init__(self):
        self.db_manager = DBManager(DB_FILENAME)
        
        # Load persistant data from db
        self.user = self.db_manager.load_db_user()
        self.book = self.db_manager.load_db_book()
        self.list_chapters = self.db_manager.load_db_chapters()

        # Flag to save data or not on db when the app is closed
        self.user_data_changed = False

        # Load GTK Window
        self.win = Window(ICON_FILE, BAR_SIZES_FILE, self)
        self.win.connect("destroy", self.win.on_destroy)
        self.win.show_all()
        
    def run(self):
        Gtk.main()