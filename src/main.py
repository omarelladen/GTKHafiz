import os

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Include config variables
exec(open('config').read())

from db_manager import DBManager
from window import Window

def main():
    db_manager = DBManager(DB_FILENAME)
    try:
        # Load persistant data from db
        user, list_books, list_chapters = db_manager.load_db_data()
        book = list_books[0]

        # Load GTK Window
        win = Window(ICON_FILE, BAR_SIZES_FILE, db_manager, user, book, list_chapters)
        win.connect("destroy", win.on_destroy)
        win.show_all()
        Gtk.main()
    except Exception as e:
        print(f"Error starting aplication: {e}")

if __name__ == '__main__':
    main()
