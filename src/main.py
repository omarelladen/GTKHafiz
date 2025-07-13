import os

import sqlite3

import configparser

def get_config_value(section, var, file):
    config = configparser.ConfigParser()
    config.read(file)
    DB_FILENAME = config[section][var]
    return DB_FILENAME

DB_FILENAME = get_config_value('db', 'DB_FILENAME', 'config')


import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk


class Book:
    def __init__(self,
        name_arabic :str = '',
        name_latin  :str = '',
        n_chapters  :int = 0,
        n_verses    :int = 0,
        n_words     :int = 0,
        n_letters   :int = 0
    ):
        self.name_arabic = name_arabic
        self.name_latin = name_latin
        self.n_chapters = n_chapters
        self.n_verses = n_verses
        self.n_words = n_words
        self.n_letters = n_letters


class Chapter:
    def __init__(self,
        number      :int = 0,
        name_arabic :str = '',
        name_latin  :str = '',
        n_verses    :str = 0,
        n_words     :int = 0,
        n_letters   :int = 0
    ):
        self.number = number
        self.name_arabic = name_arabic
        self.name_latin = name_latin
        self.n_verses = n_verses
        self.n_words = n_words
        self.n_letters = n_letters


class User:
    def __init__(self,
        username         :str = '',
        n_mem_chapters   :int = 0,
        n_mem_words      :int = 0,
        n_mem_verses     :int = 0,
        n_mem_letters    :int = 0,
        mem_chapters     :list[Chapter] = [],
    ):
        self.username = username
        self.mem_chapters = mem_chapters
        self.n_mem_chapters = n_mem_chapters
        self.n_mem_words = n_mem_words
        self.n_mem_verses = n_mem_verses
        self.n_mem_letters = n_mem_letters


class ChapterRectangle(Gdk.Rectangle):
    def __init__(self,
        x       :int = 0,
        y       :int = 0,
        width   :int = 0,
        height  :int = 0,
        chapter :int = 0,
        color   :tuple[float, float, float] = (0.0, 0.8, 0.0),
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.chapter = chapter
        self.color = color


class GTKHafizWindow(Gtk.Window):
    def __init__(self, db_manager, user, book, list_chapters):
        super().__init__()

        # Data
        self.db_manager = db_manager
        self.user = user
        self.book = book
        self.list_chapters = list_chapters

        # Window
        self.win_default_l = 350
        self.win_default_h = 400
        self.set_border_width(6)
        self.set_default_size(self.win_default_l, self.win_default_h)
        self.set_size_request(580, 550)

        # Rectangle colors
        self.rect_on_color  = (0.5, 0.5, 0.5)
        self.rect_off_color = (0.0, 0.8, 0.0)

        # Vertical Box
        outerbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(outerbox)

        # Menu Popover
        self.popover_menu = Gtk.Popover()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        bt_about = Gtk.ModelButton(label="About GTK Hafiz")
        bt_about.connect("clicked", self.on_click_about)
        vbox.pack_start(bt_about, False, True, 10)
        vbox.show_all()
        self.popover_menu.add(vbox)
        self.popover_menu.set_position(Gtk.PositionType.BOTTOM)
        
        # Header Bar
        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        headerbar.props.title = "GTK Hafiz"
        self.set_titlebar(headerbar)

        # Menu Button
        bt_menu = Gtk.MenuButton(popover=self.popover_menu)
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        bt_menu.add(image)
        headerbar.pack_end(bt_menu)

        # Stack
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        # Progress Bars
        self.pb_start_x = 10
        self.pb_start_y = 20
        self.pb_start_h = 10
        self.pb_vd = self.pb_start_h + 2
        self.pb_hd = 2
        self.list_rect_progress_bar = [
            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*0, 490, self.pb_start_h, 2),
            ChapterRectangle(self.pb_start_x+self.pb_hd+490, self.pb_start_y + self.pb_vd*0, 8, self.pb_start_h, 1),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*1, 500, self.pb_start_h, 2),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*2, 300, self.pb_start_h, 3),
            ChapterRectangle(self.pb_start_x+self.pb_hd+300, self.pb_start_y + self.pb_vd*2, 198, self.pb_start_h, 2),
            
            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*3, 120, self.pb_start_h, 4),
            ChapterRectangle(self.pb_start_x+self.pb_hd+120, self.pb_start_y + self.pb_vd*3, 378, self.pb_start_h, 3),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*4, 500, self.pb_start_h, 4),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*5, 380, self.pb_start_h, 5),
            ChapterRectangle(self.pb_start_x+self.pb_hd+380, self.pb_start_y + self.pb_vd*5, 118, self.pb_start_h, 4),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*6, 320, self.pb_start_h, 6),
            ChapterRectangle(self.pb_start_x+self.pb_hd+320, self.pb_start_y + self.pb_vd*6, 178, self.pb_start_h, 5),
    
            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*7, 260, self.pb_start_h, 7),
            ChapterRectangle(self.pb_start_x+self.pb_hd+260, self.pb_start_y + self.pb_vd*7, 238, self.pb_start_h, 6),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*8, 120, self.pb_start_h, 8),
            ChapterRectangle(self.pb_start_x+self.pb_hd+120, self.pb_start_y + self.pb_vd*8, 378, self.pb_start_h, 7),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*9, 350, self.pb_start_h, 9),
            ChapterRectangle(self.pb_start_x+self.pb_hd+350, self.pb_start_y + self.pb_vd*9, 148, self.pb_start_h, 8),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*10, 20, self.pb_start_h, 11),
            ChapterRectangle(self.pb_start_x+self.pb_hd+20, self.pb_start_y + self.pb_vd*10, 315, self.pb_start_h, 10),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+20+315, self.pb_start_y + self.pb_vd*10, 161, self.pb_start_h, 9),
            
            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*11, 160, self.pb_start_h, 12),
            ChapterRectangle(self.pb_start_x+self.pb_hd+160, self.pb_start_y + self.pb_vd*11, 338, self.pb_start_h, 11),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*12, 170, self.pb_start_h, 14),
            ChapterRectangle(self.pb_start_x+self.pb_hd+170, self.pb_start_y + self.pb_vd*12, 140, self.pb_start_h, 13),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+170+140, self.pb_start_y + self.pb_vd*12, 186, self.pb_start_h, 12),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*13, 350, self.pb_start_h, 16),
            ChapterRectangle(self.pb_start_x+self.pb_hd+350, self.pb_start_y + self.pb_vd*13, 148, self.pb_start_h, 15),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*14, 200, self.pb_start_h, 18),
            ChapterRectangle(self.pb_start_x+self.pb_hd+200, self.pb_start_y + self.pb_vd*14, 298, self.pb_start_h, 17),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*15, 220, self.pb_start_h, 20),
            ChapterRectangle(self.pb_start_x+self.pb_hd+220, self.pb_start_y + self.pb_vd*15, 170, self.pb_start_h, 19),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+220+170, self.pb_start_y + self.pb_vd*15, 106, self.pb_start_h, 18),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*16, 240, self.pb_start_h, 22),
            ChapterRectangle(self.pb_start_x+self.pb_hd+240, self.pb_start_y + self.pb_vd*16, 258, self.pb_start_h, 21),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*17, 60, self.pb_start_h, 23),
            ChapterRectangle(self.pb_start_x+self.pb_hd+60, self.pb_start_y + self.pb_vd*17, 240, self.pb_start_h, 24),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+60+240, self.pb_start_y + self.pb_vd*17, 196, self.pb_start_h, 25),
    
            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*18, 120, self.pb_start_h, 27),
            ChapterRectangle(self.pb_start_x+self.pb_hd+120, self.pb_start_y + self.pb_vd*18, 250, self.pb_start_h, 26),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+120+250, self.pb_start_y + self.pb_vd*18, 126, self.pb_start_h, 25),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*19, 130, self.pb_start_h, 29),
            ChapterRectangle(self.pb_start_x+self.pb_hd+130, self.pb_start_y + self.pb_vd*19, 270, self.pb_start_h, 28),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+130+270, self.pb_start_y + self.pb_vd*19, 96, self.pb_start_h, 27),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*20, 100, self.pb_start_h, 33),
            ChapterRectangle(self.pb_start_x+self.pb_hd+100, self.pb_start_y + self.pb_vd*20, 60, self.pb_start_h, 32),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+100+60, self.pb_start_y + self.pb_vd*20, 70, self.pb_start_h, 31),
            ChapterRectangle(self.pb_start_x+3*self.pb_hd+100+60+70, self.pb_start_y + self.pb_vd*20, 200, self.pb_start_h, 30),
            ChapterRectangle(self.pb_start_x+4*self.pb_hd+100+60+70+200, self.pb_start_y + self.pb_vd*20, 62, self.pb_start_h, 29),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*21, 40, self.pb_start_h, 36),
            ChapterRectangle(self.pb_start_x+self.pb_hd+40, self.pb_start_y + self.pb_vd*21, 140, self.pb_start_h, 35),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+40+140, self.pb_start_y + self.pb_vd*21, 120, self.pb_start_h, 34),
            ChapterRectangle(self.pb_start_x+3*self.pb_hd+40+140+120, self.pb_start_y + self.pb_vd*21, 194, self.pb_start_h, 33),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*22, 100, self.pb_start_h, 39),
            ChapterRectangle(self.pb_start_x+self.pb_hd+100, self.pb_start_y + self.pb_vd*22, 140, self.pb_start_h, 38),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+100+140, self.pb_start_y + self.pb_vd*22, 140, self.pb_start_h, 37),
            ChapterRectangle(self.pb_start_x+3*self.pb_hd+100+140+140, self.pb_start_y + self.pb_vd*22, 114, self.pb_start_h, 36),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*23, 130, self.pb_start_h, 41),
            ChapterRectangle(self.pb_start_x+self.pb_hd+130, self.pb_start_y + self.pb_vd*23, 200, self.pb_start_h, 40),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+130+200, self.pb_start_y + self.pb_vd*23, 166, self.pb_start_h, 39),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*24, 90, self.pb_start_h, 45),
            ChapterRectangle(self.pb_start_x+self.pb_hd+90, self.pb_start_y + self.pb_vd*24, 50, self.pb_start_h, 44),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+90+50, self.pb_start_y + self.pb_vd*24, 130, self.pb_start_h, 43),
            ChapterRectangle(self.pb_start_x+3*self.pb_hd+90+50+130, self.pb_start_y + self.pb_vd*24, 190, self.pb_start_h, 42),
            ChapterRectangle(self.pb_start_x+4*self.pb_hd+90+50+130+190, self.pb_start_y + self.pb_vd*24, 32, self.pb_start_h, 41),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*25, 30, self.pb_start_h, 51),
            ChapterRectangle(self.pb_start_x+self.pb_hd+30, self.pb_start_y + self.pb_vd*25, 60, self.pb_start_h, 50),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+30+60, self.pb_start_y + self.pb_vd*25, 50, self.pb_start_h, 49),
            ChapterRectangle(self.pb_start_x+3*self.pb_hd+30+60+50, self.pb_start_y + self.pb_vd*25, 110, self.pb_start_h, 48),
            ChapterRectangle(self.pb_start_x+4*self.pb_hd+30+60+50+110, self.pb_start_y + self.pb_vd*25, 140, self.pb_start_h, 47),
            ChapterRectangle(self.pb_start_x+5*self.pb_hd+30+60+50+110+140, self.pb_start_y + self.pb_vd*25, 100, self.pb_start_h, 46),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*26, 110, self.pb_start_h, 57),
            ChapterRectangle(self.pb_start_x+1*self.pb_hd+110, self.pb_start_y + self.pb_vd*26, 70, self.pb_start_h, 56),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+110+70, self.pb_start_y + self.pb_vd*26, 60, self.pb_start_h, 55),
            ChapterRectangle(self.pb_start_x+3*self.pb_hd+110+70+60, self.pb_start_y + self.pb_vd*26, 90, self.pb_start_h, 54),
            ChapterRectangle(self.pb_start_x+4*self.pb_hd+110+70+60+90, self.pb_start_y + self.pb_vd*26, 70, self.pb_start_h, 53),
            ChapterRectangle(self.pb_start_x+5*self.pb_hd+110+70+60+90+70, self.pb_start_y + self.pb_vd*26, 40, self.pb_start_h, 52),
            ChapterRectangle(self.pb_start_x+6*self.pb_hd+110+70+60+90+70+40, self.pb_start_y + self.pb_vd*26, 48, self.pb_start_h, 51),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*27, 40, self.pb_start_h, 66),
            ChapterRectangle(self.pb_start_x+1*self.pb_hd+40, self.pb_start_y + self.pb_vd*27, 50, self.pb_start_h, 65),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+40+50,self.pb_start_y + self.pb_vd*27, 40, self.pb_start_h, 64),
            ChapterRectangle(self.pb_start_x+3*self.pb_hd+40+50+40, self.pb_start_y + self.pb_vd*27, 30, self.pb_start_h, 63),
            ChapterRectangle(self.pb_start_x+4*self.pb_hd+40+50+40+30, self.pb_start_y + self.pb_vd*27, 30, self.pb_start_h, 62),
            ChapterRectangle(self.pb_start_x+5*self.pb_hd+40+50+40+30+30, self.pb_start_y + self.pb_vd*27, 40, self.pb_start_h, 61),
            ChapterRectangle(self.pb_start_x+6*self.pb_hd+40+50+40+30+30+40, self.pb_start_y + self.pb_vd*27, 70, self.pb_start_h, 60),
            ChapterRectangle(self.pb_start_x+7*self.pb_hd+40+50+40+30+30+40+70, self.pb_start_y + self.pb_vd*27, 100, self.pb_start_h, 59),
            ChapterRectangle(self.pb_start_x+8*self.pb_hd+40+50+40+30+30+40+70+100, self.pb_start_y + self.pb_vd*27, 84, self.pb_start_h, 58),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 77),
            ChapterRectangle(self.pb_start_x +1*self.pb_hd+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 76),
            ChapterRectangle(self.pb_start_x +2*self.pb_hd+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 75),
            ChapterRectangle(self.pb_start_x +3*self.pb_hd+30+40+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 74),
            ChapterRectangle(self.pb_start_x +4*self.pb_hd+30+40+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 73),
            ChapterRectangle(self.pb_start_x +5*self.pb_hd+30+40+30+40+30, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 72),
            ChapterRectangle(self.pb_start_x +6*self.pb_hd+30+40+30+40+30+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 71),
            ChapterRectangle(self.pb_start_x +7*self.pb_hd+30+40+30+40+30+50+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 70),
            ChapterRectangle(self.pb_start_x +8*self.pb_hd+30+40+30+40+30+50+50+50, self.pb_start_y + self.pb_vd*28, 60, self.pb_start_h, 69),
            ChapterRectangle(self.pb_start_x +9*self.pb_hd+30+40+30+40+30+50+50+50+60, self.pb_start_y + self.pb_vd*28, 60, self.pb_start_h, 68),
            ChapterRectangle(self.pb_start_x+10*self.pb_hd+30+40+30+40+30+50+50+50+60+60, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 67),

            ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*29, 20, self.pb_start_h, 86),
            ChapterRectangle(self.pb_start_x+1*self.pb_hd+20, self.pb_start_y + self.pb_vd*29, 45, self.pb_start_h, 85),
            ChapterRectangle(self.pb_start_x+2*self.pb_hd+20+45, self.pb_start_y + self.pb_vd*29, 45, self.pb_start_h, 84),
            ChapterRectangle(self.pb_start_x+3*self.pb_hd+20+45+45, self.pb_start_y + self.pb_vd*29, 80, self.pb_start_h, 83),
            ChapterRectangle(self.pb_start_x+4*self.pb_hd+20+45+45+80, self.pb_start_y + self.pb_vd*29, 30, self.pb_start_h, 82),
            ChapterRectangle(self.pb_start_x+5*self.pb_hd+20+45+45+80+30, self.pb_start_y + self.pb_vd*29, 40, self.pb_start_h, 81),
            ChapterRectangle(self.pb_start_x+6*self.pb_hd+20+45+45+80+30+40, self.pb_start_y + self.pb_vd*29, 70, self.pb_start_h, 80),
            ChapterRectangle(self.pb_start_x+7*self.pb_hd+20+45+45+80+30+40+70, self.pb_start_y + self.pb_vd*29, 80, self.pb_start_h, 79),
            ChapterRectangle(self.pb_start_x+8*self.pb_hd+20+45+45+80+30+40+70+80, self.pb_start_y + self.pb_vd*29, 74, self.pb_start_h, 78),

            # ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 77),
            # ChapterRectangle(self.pb_start_x +1*self.pb_hd+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 76),
            # ChapterRectangle(self.pb_start_x +2*self.pb_hd+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 75),
            # ChapterRectangle(self.pb_start_x +3*self.pb_hd+30+40+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 74),
            # ChapterRectangle(self.pb_start_x +4*self.pb_hd+30+40+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 73),
            # ChapterRectangle(self.pb_start_x +5*self.pb_hd+30+40+30+40+30, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 72),
            # ChapterRectangle(self.pb_start_x +6*self.pb_hd+30+40+30+40+30+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 71),
            # ChapterRectangle(self.pb_start_x +7*self.pb_hd+30+40+30+40+30+50+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 70),
            # ChapterRectangle(self.pb_start_x +8*self.pb_hd+30+40+30+40+30+50+50+50, self.pb_start_y + self.pb_vd*28, 60, self.pb_start_h, 69),
            # ChapterRectangle(self.pb_start_x +9*self.pb_hd+30+40+30+40+30+50+50+50+60, self.pb_start_y + self.pb_vd*28, 60, self.pb_start_h, 68),
            # ChapterRectangle(self.pb_start_x+10*self.pb_hd+30+40+30+40+30+50+50+50+60+60, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 67),
            # ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 77),
            # ChapterRectangle(self.pb_start_x +1*self.pb_hd+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 76),
            # ChapterRectangle(self.pb_start_x +2*self.pb_hd+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 75),
            # ChapterRectangle(self.pb_start_x +3*self.pb_hd+30+40+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 74),
            # ChapterRectangle(self.pb_start_x +4*self.pb_hd+30+40+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 73),
            # ChapterRectangle(self.pb_start_x +5*self.pb_hd+30+40+30+40+30, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 72),
            # ChapterRectangle(self.pb_start_x +6*self.pb_hd+30+40+30+40+30+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 71),
            # ChapterRectangle(self.pb_start_x +7*self.pb_hd+30+40+30+40+30+50+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 70),
            # ChapterRectangle(self.pb_start_x +8*self.pb_hd+30+40+30+40+30+50+50+50, self.pb_start_y + self.pb_vd*28, 60, self.pb_start_h, 69),
            # ChapterRectangle(self.pb_start_x +9*self.pb_hd+30+40+30+40+30+50+50+50+60, self.pb_start_y + self.pb_vd*28, 60, self.pb_start_h, 68),
            # ChapterRectangle(self.pb_start_x+10*self.pb_hd+30+40+30+40+30+50+50+50+60+60, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 67),
            # ChapterRectangle(self.pb_start_x, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 77),
            # ChapterRectangle(self.pb_start_x +1*self.pb_hd+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 76),
            # ChapterRectangle(self.pb_start_x +2*self.pb_hd+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 75),
            # ChapterRectangle(self.pb_start_x +3*self.pb_hd+30+40+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 74),
            # ChapterRectangle(self.pb_start_x +4*self.pb_hd+30+40+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 73),
            # ChapterRectangle(self.pb_start_x +5*self.pb_hd+30+40+30+40+30, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 72),
            # ChapterRectangle(self.pb_start_x +6*self.pb_hd+30+40+30+40+30+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 71),
            # ChapterRectangle(self.pb_start_x +7*self.pb_hd+30+40+30+40+30+50+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 70),
        ]

        # Progress Bar Tab
        drawingarea_progress_bar = Gtk.DrawingArea()
        drawingarea_progress_bar.connect("draw", self.on_draw_progress_bar)
        drawingarea_progress_bar.connect("button-press-event", self.on_click_progress_bar)
        drawingarea_progress_bar.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        stack.add_titled(drawingarea_progress_bar, "bar", "Bar")

        # Matrix Tab
        self.rects_per_col  = 19
        self.rects_per_line = 6
        self.list_rect_matrix = []
        drawingarea_matrix = Gtk.DrawingArea()
        drawingarea_matrix.connect("draw", self.on_draw_matrix)
        drawingarea_matrix.connect("button-press-event", self.on_click_matrix)
        drawingarea_matrix.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        stack.add_titled(drawingarea_matrix, "matrix", "Matrix")

        # Create Rectangles for Progress Bar and Matrix
        self.refresh_rectangles()

        # List Tab
        checkbutton_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.list_checkboxes = []
        for chapter in self.list_chapters:
            checkbutton = Gtk.CheckButton(label=f"{chapter.number}. ({chapter.name_latin}) {chapter.name_arabic}")
            if chapter.number in self.user.mem_chapters:
                checkbutton.set_active(True)
            self.list_checkboxes.append((checkbutton, chapter))
            checkbutton.connect("toggled", lambda btn, obj=chapter: self.on_toggle_checkbox(btn, obj))
            checkbutton_container.pack_start(checkbutton, False, False, 0)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(checkbutton_container)
        stack.add_titled(scrolled_window, "list", "List")

        # Stats Tab
        self.label_stats = Gtk.Label()
        self.refresh_stats_label()
        stack.add_titled(self.label_stats, "stats", "Statistics")

        # Chapter Popover
        self.popover_chapter = Gtk.Popover()
        self.label_chapter = Gtk.Label()
        self.popover_chapter.add(self.label_chapter)

        self.is_popover_chapter_active = False
        self.cursor_when_popover_chapter_x = None
        self.cursor_when_popover_chapter_y = None

        # All clicks will be checked to be able to hide the chapter popovers
        self.connect("button-press-event", self.on_click_outside_popover)

        # Stack Switcher
        stackswitcher = Gtk.StackSwitcher()
        stackswitcher.set_stack(stack)
        stackswitcher.set_halign(Gtk.Align.CENTER)  # horizontal

        outerbox.pack_start(stackswitcher, False, True, 0)
        outerbox.pack_start(stack, True, True, 0)

    def on_click_outside_popover(self, widget, event):
        if (self.is_popover_chapter_active == True and
            event.x != self.cursor_when_popover_chapter_x and
            event.y != self.cursor_when_popover_chapter_y):
            self.is_popover_chapter_active = False
            self.popover_chapter.hide()

    def on_click_progress_bar(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == Gdk.BUTTON_PRIMARY:
                for rect in self.list_rect_progress_bar:
                    if (rect.x <= event.x <= rect.x + rect.width and
                        rect.y <= event.y <= rect.y + rect.height):
                        self.show_chapter_popover(rect, widget, event)
                        break

    def on_click_matrix(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == Gdk.BUTTON_PRIMARY:
                e_x, e_y = event.x, event.y
                for rect in self.list_rect_matrix:
                    r_x = rect.x
                    r_y = rect.y
                    r_w = rect.width
                    r_h = rect.height
                    if r_x <= e_x <= r_x + r_w and r_y <= e_y <= r_y + r_h:
                        self.show_chapter_popover(rect, widget, event)
                        break

    def on_click_about(self, widget):
        about = Gtk.AboutDialog(transient_for=self, modal=True)

        about.set_program_name("GTK Hafiz")
        about.set_version("0.0")
        about.set_comments("Track Qur'an memorization visualy")
        about.set_website("https://github.com/omarelladen")
        about.set_website_label("Repository")
        about.set_authors(["Omar El Laden"])
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_copyright("Copyright © 2025 Omar El Laden")
        about.set_logo_icon_name("application-x-executable")

        about.connect("response", lambda dialog, response: dialog.destroy())
        about.present()

    def on_toggle_checkbox(self, button, chapter=''):
        # Checkbox activation
        if button.get_active():
            self.user.mem_chapters.append(chapter.number)
            self.user.n_mem_chapters += 1
            self.user.n_mem_verses   += chapter.n_verses
            self.user.n_mem_words    += chapter.n_words
            self.user.n_mem_letters  += chapter.n_letters
            self.db_manager.save_mem_chapters(self.user, chapter, 'add')
        # Checkbox deactivation
        else:
            self.user.mem_chapters.remove(chapter.number)
            self.user.n_mem_chapters -= 1
            self.user.n_mem_verses   -= chapter.n_verses
            self.user.n_mem_words    -= chapter.n_words
            self.user.n_mem_letters  -= chapter.n_letters
            self.db_manager.save_mem_chapters(self.user, chapter, 'rm')
        
        # Refresh
        self.refresh_stats_label()
        self.refresh_rectangles()

    def on_draw_matrix(self, widget, cr):
        for rect in self.list_rect_matrix:
            r_x = rect.x
            r_y = rect.y
            r_w = rect.width
            r_h = rect.height
            r_color = rect.color
            cr.set_source_rgb(r_color[0], r_color[1], r_color[2])
            cr.rectangle(r_x, r_y, r_w, r_h)
            cr.fill()

    def on_draw_progress_bar(self, widget, cr):
        for rect in self.list_rect_progress_bar:
            cr.set_source_rgb(*rect.color)
            cr.rectangle(rect.x, rect.y, rect.width, rect.height)
            cr.fill()

    def show_chapter_popover(self, rect, widget, event):
        self.label_chapter.set_text(f"{rect.chapter}")
        e_x = event.x
        e_y = event.y

        # Set popover position
        self.popover_chapter.set_relative_to(widget)
        self.popover_chapter.set_pointing_to(rect)
        self.popover_chapter.set_position(Gtk.PositionType.TOP)
        self.popover_chapter.show_all()

        # Set current popover location and state so that it is gets hiden only by clicking outside this point
        self.cursor_when_popover_chapter_x = e_x
        self.cursor_when_popover_chapter_y = e_y
        self.is_popover_chapter_active = True

    def refresh_rectangles(self):
        # Refresh Matrix Rectangles
        self.list_rect_matrix = [] # updates rectangle colors by creating a new list
        for i in range(self.rects_per_col):
            for j in range(self.rects_per_line):
                x = 155+ (self.rects_per_line-1-j) * 35 # from left to right
                y = 15 + i * 20
                chapter_num = i * (self.rects_per_line) + j + 1
                r, g, b = self.rect_off_color if chapter_num in self.user.mem_chapters else self.rect_on_color
                self.list_rect_matrix.append(ChapterRectangle(x, y, 30, 10, chapter_num, (r, g, b)))

        # Refresh Progress Bar Rectangles
        for rect in self.list_rect_progress_bar:
            rect.color = self.rect_off_color if rect.chapter in self.user.mem_chapters else self.rect_on_color
        
        # Ensure Redraw
        self.queue_draw() 

    def refresh_stats_label(self):
        self.label_stats.set_markup(
            f"<big><b>Username:</b> {self.user.username}</big>\n\n"
            f"<big><b>Chapters:</b> {self.user.n_mem_chapters} ({round(self.user.n_mem_chapters / self.book.n_chapters * 100, 1)}%)</big>\n"
            f"<big><b>Verses:</b> {self.user.n_mem_verses} ({round(self.user.n_mem_verses / self.book.n_verses * 100, 1)}%)</big>\n"
            f"<big><b>Words:</b> {self.user.n_mem_words} ({round(self.user.n_mem_words / self.book.n_words * 100, 1)}%)</big>\n"
            f"<big><b>Letters:</b> {self.user.n_mem_letters} ({round(self.user.n_mem_letters / self.book.n_letters * 100, 1)}%)</big>"
        )


class DBManager():
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def __load_db_books(self, cur):
        db_table_books = [a for a in cur.execute("SELECT * FROM books")]
        list_books=[]
        for b in db_table_books:
            list_books.append(Book(b[1], b[2], b[3], b[4], b[5], b[6]))
        return list_books

    def __load_db_chapters(self, cur):
        db_table_chapters = [a for a in cur.execute("SELECT * FROM chapters")]
        list_chapters=[]
        for c in db_table_chapters:
            list_chapters.append(Chapter(c[0], c[1], c[2], c[3], c[4], c[5]))
        return list_chapters

    def __load_db_user(self, cur):
        db_table_users = [a for a in cur.execute("SELECT * FROM users")]
        if len(db_table_users) > 0:
            list_users =[]
            for u in db_table_users:
                list_users.append(User(u[0], u[1], u[2], u[3], u[4]))
            user = list_users[0]

            db_table_users_mem_chapters = [a for a in cur.execute("SELECT * FROM mem_chapters")]
            for t in db_table_users_mem_chapters:
                user.mem_chapters.append(t[1])
        else:
            username = os.getlogin()
            user = User(username)

            cur.execute("""
                INSERT INTO users
                (username, n_mem_chapters, n_mem_words, n_mem_verses, n_mem_letters) VALUES (?, ?, ?, ?, ?)
                """, (user.username, user.n_mem_chapters, user.n_mem_words, user.n_mem_verses, user.n_mem_letters))
        return user

    def load_db_data(self):
        con = sqlite3.connect(self.db_filename)
        cur = con.cursor()

        list_books    = self.__load_db_books(cur)
        list_chapters = self.__load_db_chapters(cur)
        user          = self.__load_db_user(cur)
        
        con.commit()
        con.close()

        return user, list_books, list_chapters

    def save_mem_chapters(self, user:User, chapter:Chapter, op:str):
            con = sqlite3.connect(self.db_filename)
            cur = con.cursor()

            cur.execute("""
                UPDATE users
                SET n_mem_chapters = ?, n_mem_verses = ?, n_mem_words = ?, n_mem_letters = ?
                WHERE username = ?
            """, (user.n_mem_chapters, user.n_mem_verses, user.n_mem_words, user.n_mem_letters, user.username))

            if op == 'add':
                cur.execute("""
                    INSERT INTO mem_chapters
                    (users_username, chapters_number) VALUES (?, ?)
                """, (user.username, chapter.number))
            elif op == 'rm':
                cur.execute("""
                    DELETE FROM mem_chapters
                    WHERE users_username = ? AND
                        chapters_number = ?
                """, (user.username, chapter.number))

            con.commit()
            con.close()


def main():
    # Load persistant data from db
    db_manager = DBManager(DB_FILENAME)
    user, list_books, list_chapters = db_manager.load_db_data()
    book = list_books[0]

    # Load GTK Window
    win = GTKHafizWindow(db_manager, user, book, list_chapters)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()
