import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Include config variables
exec(open('config').read())

from db_manager import DBManager
from window import Window

def main():
    # Load persistant data from db
    db_manager = DBManager(DB_FILENAME)
    user, list_books, list_chapters = db_manager.load_db_data()
    book = list_books[0]

    # Load GTK Window
    win = Window(db_manager, user, book, list_chapters)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()
