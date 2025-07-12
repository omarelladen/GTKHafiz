import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk,Gio,Gdk,GdkPixbuf

import sqlite3
dbfile = 'db.sqlite3'

import os


class Book:
    def __init__(self,
        name_arabic :str = '',
        name_latin  :str = '',
        # author      :str = '',
        n_chapters  :int = 0,
        n_verses    :int = 0,
        n_words     :int = 0,
        n_letters   :int = 0
    ):
        self.name_arabic = name_arabic
        self.name_latin = name_latin
        # self.author = author
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
        # pct_mem_chapters :int = 0,
        # pct_mem_words    :int = 0,
        # pct_mem_verses   :int = 0,
        # pct_mem_letters  :int = 0,
        mem_chapters     :list = [],
        mem_words        :list = [],
        mem_verses       :list = [],
        # mem_letters      :list = []
    ):
        self.username = username
        self.mem_chapters = mem_chapters
        self.n_mem_chapters = n_mem_chapters
        self.n_mem_words = n_mem_words
        self.n_mem_verses = n_mem_verses
        self.n_mem_letters = n_mem_letters
        # self.pct_mem_chapters = pct_mem_chapters
        # self.pct_mem_words = pct_mem_words
        # self.pct_mem_verses = n_mem_verses
        # self.pct_mem_letters= n_mem_letters
        # self.mem_words = mem_words
        # self.mem_verses = mem_verses
        # self.mem_letters = mem_letters
        # self.mem_letters = mem_letters

    def calc_pct_mem_chapters(self) -> float:
        return round(self.n_mem_chapters / book.n_chapters * 100, 1)
    def calc_pct_mem_words(self) -> float:
        return round(self.n_mem_words / book.n_words * 100, 1)
    def calc_pct_mem_verses(self) -> float:
        return round(self.n_mem_verses / book.n_verses * 100, 1)
    def calc_pct_mem_letters(self) -> float:
        return round(self.n_mem_letters / book.n_letters * 100, 1)


class ProgressBar:
    def __init__(self,
        x       :int = 0,
        y       :int = 0,
        width   :int = 0,
        height  :int = 0,
        chapter :int = 0,
        color   :int = (0.0, 0.8, 0.0),
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.chapter = chapter
        self.color = color


class GTKHafizWindow(Gtk.Window):
    def __init__(self):
        super().__init__()

        ## Window
        self.win_default_l = 350
        self.win_default_h = 400
        self.set_border_width(6)
        self.set_default_size(self.win_default_l, self.win_default_h)

        self.set_size_request(580, 550)
        # print(self.get_size())

        self.color_c1  = (255/255, 255/255, 255/255)
        self.color_c2  = (255/255, 255/255, 255/255)
        self.color_c3  = (255/255, 255/255, 255/255)
        self.color_c4  = (255/255, 255/255, 255/255)
        self.color_c5  = (255/255, 255/255, 255/255)
        self.color_c6  = (255/255, 255/255, 255/255)
        self.color_c7  = (255/255, 255/255, 255/255)
        self.color_c8  = (255/255, 255/255, 255/255)
        self.color_c9  = (255/255, 255/255, 255/255)
        self.color_c10 = (255/255, 255/255, 255/255)
        self.color_c11 = (255/255, 255/255, 255/255)
        self.color_c12 = (255/255, 255/255, 255/255)
        self.color_c13 = (255/255, 255/255, 255/255)
        self.color_c14 = (255/255, 255/255, 255/255)


        self.on_color  = (0.5, 0.5, 0.5)
        self.off_color = (0.0, 0.8, 0.0)


        ## Vertical Box
        outerbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(outerbox)

        # Menu Popover
        self.popover = Gtk.Popover()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # bt_preferences = Gtk.ModelButton(label="Preferences")
        # vbox.pack_start(bt_preferences, False, True, 10)
        bt_about = Gtk.ModelButton(label="About GTK Hafiz")
        bt_about.connect("clicked", self.on_about_clicked)
        vbox.pack_start(bt_about, False, True, 10)
        vbox.show_all()
        self.popover.add(vbox)
        self.popover.set_position(Gtk.PositionType.BOTTOM)
        

        ## Header Bar
        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        headerbar.props.title = "GTK Hafiz"
        self.set_titlebar(headerbar)

        # Menu Button
        bt_menu = Gtk.MenuButton(popover=self.popover)
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        bt_menu.add(image)
        headerbar.pack_end(bt_menu)


        ## Stack
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)


        ## Progress Bar Tab with DrawingArea
        self.pb_start_x = 10
        self.pb_start_y = 20
        self.pb_start_h = 10
        self.pb_vd = self.pb_start_h + 2
        self.pb_hd = 2
        self.rectangles_progress_bar = [
            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*0, 490, self.pb_start_h, 2),
            ProgressBar(self.pb_start_x+self.pb_hd+490, self.pb_start_y + self.pb_vd*0, 8, self.pb_start_h, 1),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*1, 500, self.pb_start_h, 2),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*2, 300, self.pb_start_h, 3),
            ProgressBar(self.pb_start_x+self.pb_hd+300, self.pb_start_y + self.pb_vd*2, 198, self.pb_start_h, 2),
            
            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*3, 120, self.pb_start_h, 4),
            ProgressBar(self.pb_start_x+self.pb_hd+120, self.pb_start_y + self.pb_vd*3, 378, self.pb_start_h, 3),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*4, 500, self.pb_start_h, 4),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*5, 380, self.pb_start_h, 5),
            ProgressBar(self.pb_start_x+self.pb_hd+380, self.pb_start_y + self.pb_vd*5, 118, self.pb_start_h, 4),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*6, 320, self.pb_start_h, 6),
            ProgressBar(self.pb_start_x+self.pb_hd+320, self.pb_start_y + self.pb_vd*6, 178, self.pb_start_h, 5),
    
            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*7, 260, self.pb_start_h, 7),
            ProgressBar(self.pb_start_x+self.pb_hd+260, self.pb_start_y + self.pb_vd*7, 238, self.pb_start_h, 6),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*8, 120, self.pb_start_h, 8),
            ProgressBar(self.pb_start_x+self.pb_hd+120, self.pb_start_y + self.pb_vd*8, 378, self.pb_start_h, 7),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*9, 350, self.pb_start_h, 9),
            ProgressBar(self.pb_start_x+self.pb_hd+350, self.pb_start_y + self.pb_vd*9, 148, self.pb_start_h, 8),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*10, 20, self.pb_start_h, 11),
            ProgressBar(self.pb_start_x+self.pb_hd+20, self.pb_start_y + self.pb_vd*10, 315, self.pb_start_h, 10),
            ProgressBar(self.pb_start_x+2*self.pb_hd+20+315, self.pb_start_y + self.pb_vd*10, 161, self.pb_start_h, 9),
            
            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*11, 160, self.pb_start_h, 12),
            ProgressBar(self.pb_start_x+self.pb_hd+160, self.pb_start_y + self.pb_vd*11, 338, self.pb_start_h, 11),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*12, 170, self.pb_start_h, 14),
            ProgressBar(self.pb_start_x+self.pb_hd+170, self.pb_start_y + self.pb_vd*12, 140, self.pb_start_h, 13),
            ProgressBar(self.pb_start_x+2*self.pb_hd+170+140, self.pb_start_y + self.pb_vd*12, 186, self.pb_start_h, 12),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*13, 350, self.pb_start_h, 16),
            ProgressBar(self.pb_start_x+self.pb_hd+350, self.pb_start_y + self.pb_vd*13, 148, self.pb_start_h, 15),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*14, 200, self.pb_start_h, 18),
            ProgressBar(self.pb_start_x+self.pb_hd+200, self.pb_start_y + self.pb_vd*14, 298, self.pb_start_h, 17),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*15, 220, self.pb_start_h, 20),
            ProgressBar(self.pb_start_x+self.pb_hd+220, self.pb_start_y + self.pb_vd*15, 170, self.pb_start_h, 19),
            ProgressBar(self.pb_start_x+2*self.pb_hd+220+170, self.pb_start_y + self.pb_vd*15, 106, self.pb_start_h, 18),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*16, 240, self.pb_start_h, 22),
            ProgressBar(self.pb_start_x+self.pb_hd+240, self.pb_start_y + self.pb_vd*16, 258, self.pb_start_h, 21),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*17, 60, self.pb_start_h, 23),
            ProgressBar(self.pb_start_x+self.pb_hd+60, self.pb_start_y + self.pb_vd*17, 240, self.pb_start_h, 24),
            ProgressBar(self.pb_start_x+2*self.pb_hd+60+240, self.pb_start_y + self.pb_vd*17, 196, self.pb_start_h, 25),
    
            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*18, 120, self.pb_start_h, 27),
            ProgressBar(self.pb_start_x+self.pb_hd+120, self.pb_start_y + self.pb_vd*18, 250, self.pb_start_h, 26),
            ProgressBar(self.pb_start_x+2*self.pb_hd+120+250, self.pb_start_y + self.pb_vd*18, 126, self.pb_start_h, 25),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*19, 130, self.pb_start_h, 29),
            ProgressBar(self.pb_start_x+self.pb_hd+130, self.pb_start_y + self.pb_vd*19, 270, self.pb_start_h, 28),
            ProgressBar(self.pb_start_x+2*self.pb_hd+130+270, self.pb_start_y + self.pb_vd*19, 96, self.pb_start_h, 27),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*20, 100, self.pb_start_h, 33),
            ProgressBar(self.pb_start_x+self.pb_hd+100, self.pb_start_y + self.pb_vd*20, 60, self.pb_start_h, 32),
            ProgressBar(self.pb_start_x+2*self.pb_hd+100+60, self.pb_start_y + self.pb_vd*20, 70, self.pb_start_h, 31),
            ProgressBar(self.pb_start_x+3*self.pb_hd+100+60+70, self.pb_start_y + self.pb_vd*20, 200, self.pb_start_h, 30),
            ProgressBar(self.pb_start_x+4*self.pb_hd+100+60+70+200, self.pb_start_y + self.pb_vd*20, 62, self.pb_start_h, 29),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*21, 40, self.pb_start_h, 36),
            ProgressBar(self.pb_start_x+self.pb_hd+40, self.pb_start_y + self.pb_vd*21, 140, self.pb_start_h, 35),
            ProgressBar(self.pb_start_x+2*self.pb_hd+40+140, self.pb_start_y + self.pb_vd*21, 120, self.pb_start_h, 34),
            ProgressBar(self.pb_start_x+3*self.pb_hd+40+140+120, self.pb_start_y + self.pb_vd*21, 194, self.pb_start_h, 33),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*22, 100, self.pb_start_h, 39),
            ProgressBar(self.pb_start_x+self.pb_hd+100, self.pb_start_y + self.pb_vd*22, 140, self.pb_start_h, 38),
            ProgressBar(self.pb_start_x+2*self.pb_hd+100+140, self.pb_start_y + self.pb_vd*22, 140, self.pb_start_h, 37),
            ProgressBar(self.pb_start_x+3*self.pb_hd+100+140+140, self.pb_start_y + self.pb_vd*22, 114, self.pb_start_h, 36),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*23, 130, self.pb_start_h, 41),
            ProgressBar(self.pb_start_x+self.pb_hd+130, self.pb_start_y + self.pb_vd*23, 200, self.pb_start_h, 40),
            ProgressBar(self.pb_start_x+2*self.pb_hd+130+200, self.pb_start_y + self.pb_vd*23, 166, self.pb_start_h, 39),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*24, 90, self.pb_start_h, 45),
            ProgressBar(self.pb_start_x+self.pb_hd+90, self.pb_start_y + self.pb_vd*24, 50, self.pb_start_h, 44),
            ProgressBar(self.pb_start_x+2*self.pb_hd+90+50, self.pb_start_y + self.pb_vd*24, 130, self.pb_start_h, 43),
            ProgressBar(self.pb_start_x+3*self.pb_hd+90+50+130, self.pb_start_y + self.pb_vd*24, 190, self.pb_start_h, 42),
            ProgressBar(self.pb_start_x+4*self.pb_hd+90+50+130+190, self.pb_start_y + self.pb_vd*24, 32, self.pb_start_h, 41),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*25, 30, self.pb_start_h, 51),
            ProgressBar(self.pb_start_x+self.pb_hd+30, self.pb_start_y + self.pb_vd*25, 60, self.pb_start_h, 50),
            ProgressBar(self.pb_start_x+2*self.pb_hd+30+60, self.pb_start_y + self.pb_vd*25, 50, self.pb_start_h, 49),
            ProgressBar(self.pb_start_x+3*self.pb_hd+30+60+50, self.pb_start_y + self.pb_vd*25, 110, self.pb_start_h, 48),
            ProgressBar(self.pb_start_x+4*self.pb_hd+30+60+50+110, self.pb_start_y + self.pb_vd*25, 140, self.pb_start_h, 47),
            ProgressBar(self.pb_start_x+5*self.pb_hd+30+60+50+110+140, self.pb_start_y + self.pb_vd*25, 100, self.pb_start_h, 46),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*26, 110, self.pb_start_h, 57),
            ProgressBar(self.pb_start_x+1*self.pb_hd+110, self.pb_start_y + self.pb_vd*26, 70, self.pb_start_h, 56),
            ProgressBar(self.pb_start_x+2*self.pb_hd+110+70, self.pb_start_y + self.pb_vd*26, 60, self.pb_start_h, 55),
            ProgressBar(self.pb_start_x+3*self.pb_hd+110+70+60, self.pb_start_y + self.pb_vd*26, 90, self.pb_start_h, 54),
            ProgressBar(self.pb_start_x+4*self.pb_hd+110+70+60+90, self.pb_start_y + self.pb_vd*26, 70, self.pb_start_h, 53),
            ProgressBar(self.pb_start_x+5*self.pb_hd+110+70+60+90+70, self.pb_start_y + self.pb_vd*26, 40, self.pb_start_h, 52),
            ProgressBar(self.pb_start_x+6*self.pb_hd+110+70+60+90+70+40, self.pb_start_y + self.pb_vd*26, 48, self.pb_start_h, 51),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*27, 40, self.pb_start_h, 66),
            ProgressBar(self.pb_start_x+1*self.pb_hd+40, self.pb_start_y + self.pb_vd*27, 50, self.pb_start_h, 65),
            ProgressBar(self.pb_start_x+2*self.pb_hd+40+50,self.pb_start_y + self.pb_vd*27, 40, self.pb_start_h, 64),
            ProgressBar(self.pb_start_x+3*self.pb_hd+40+50+40, self.pb_start_y + self.pb_vd*27, 30, self.pb_start_h, 63),
            ProgressBar(self.pb_start_x+4*self.pb_hd+40+50+40+30, self.pb_start_y + self.pb_vd*27, 30, self.pb_start_h, 62),
            ProgressBar(self.pb_start_x+5*self.pb_hd+40+50+40+30+30, self.pb_start_y + self.pb_vd*27, 40, self.pb_start_h, 61),
            ProgressBar(self.pb_start_x+6*self.pb_hd+40+50+40+30+30+40, self.pb_start_y + self.pb_vd*27, 70, self.pb_start_h, 60),
            ProgressBar(self.pb_start_x+7*self.pb_hd+40+50+40+30+30+40+70, self.pb_start_y + self.pb_vd*27, 100, self.pb_start_h, 59),
            ProgressBar(self.pb_start_x+8*self.pb_hd+40+50+40+30+30+40+70+100, self.pb_start_y + self.pb_vd*27, 84, self.pb_start_h, 58),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 77),
            ProgressBar(self.pb_start_x +1*self.pb_hd+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 76),
            ProgressBar(self.pb_start_x +2*self.pb_hd+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 75),
            ProgressBar(self.pb_start_x +3*self.pb_hd+30+40+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 74),
            ProgressBar(self.pb_start_x +4*self.pb_hd+30+40+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 73),
            ProgressBar(self.pb_start_x +5*self.pb_hd+30+40+30+40+30, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 72),
            ProgressBar(self.pb_start_x +6*self.pb_hd+30+40+30+40+30+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 71),
            ProgressBar(self.pb_start_x +7*self.pb_hd+30+40+30+40+30+50+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 70),
            ProgressBar(self.pb_start_x +8*self.pb_hd+30+40+30+40+30+50+50+50, self.pb_start_y + self.pb_vd*28, 60, self.pb_start_h, 69),
            ProgressBar(self.pb_start_x +9*self.pb_hd+30+40+30+40+30+50+50+50+60, self.pb_start_y + self.pb_vd*28, 60, self.pb_start_h, 68),
            ProgressBar(self.pb_start_x+10*self.pb_hd+30+40+30+40+30+50+50+50+60+60, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 67),

            ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*29, 20, self.pb_start_h, 86),
            ProgressBar(self.pb_start_x+1*self.pb_hd+20, self.pb_start_y + self.pb_vd*29, 45, self.pb_start_h, 85),
            ProgressBar(self.pb_start_x+2*self.pb_hd+20+45, self.pb_start_y + self.pb_vd*29, 45, self.pb_start_h, 84),
            ProgressBar(self.pb_start_x+3*self.pb_hd+20+45+45, self.pb_start_y + self.pb_vd*29, 80, self.pb_start_h, 83),
            ProgressBar(self.pb_start_x+4*self.pb_hd+20+45+45+80, self.pb_start_y + self.pb_vd*29, 30, self.pb_start_h, 82),
            ProgressBar(self.pb_start_x+5*self.pb_hd+20+45+45+80+30, self.pb_start_y + self.pb_vd*29, 40, self.pb_start_h, 81),
            ProgressBar(self.pb_start_x+6*self.pb_hd+20+45+45+80+30+40, self.pb_start_y + self.pb_vd*29, 70, self.pb_start_h, 80),
            ProgressBar(self.pb_start_x+7*self.pb_hd+20+45+45+80+30+40+70, self.pb_start_y + self.pb_vd*29, 80, self.pb_start_h, 79),
            ProgressBar(self.pb_start_x+8*self.pb_hd+20+45+45+80+30+40+70+80, self.pb_start_y + self.pb_vd*29, 74, self.pb_start_h, 78),

            # ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 77),
            # ProgressBar(self.pb_start_x +1*self.pb_hd+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 76),
            # ProgressBar(self.pb_start_x +2*self.pb_hd+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 75),
            # ProgressBar(self.pb_start_x +3*self.pb_hd+30+40+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 74),
            # ProgressBar(self.pb_start_x +4*self.pb_hd+30+40+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 73),
            # ProgressBar(self.pb_start_x +5*self.pb_hd+30+40+30+40+30, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 72),
            # ProgressBar(self.pb_start_x +6*self.pb_hd+30+40+30+40+30+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 71),
            # ProgressBar(self.pb_start_x +7*self.pb_hd+30+40+30+40+30+50+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 70),
            # ProgressBar(self.pb_start_x +8*self.pb_hd+30+40+30+40+30+50+50+50, self.pb_start_y + self.pb_vd*28, 60, self.pb_start_h, 69),
            # ProgressBar(self.pb_start_x +9*self.pb_hd+30+40+30+40+30+50+50+50+60, self.pb_start_y + self.pb_vd*28, 60, self.pb_start_h, 68),
            # ProgressBar(self.pb_start_x+10*self.pb_hd+30+40+30+40+30+50+50+50+60+60, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 67),
            # ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 77),
            # ProgressBar(self.pb_start_x +1*self.pb_hd+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 76),
            # ProgressBar(self.pb_start_x +2*self.pb_hd+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 75),
            # ProgressBar(self.pb_start_x +3*self.pb_hd+30+40+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 74),
            # ProgressBar(self.pb_start_x +4*self.pb_hd+30+40+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 73),
            # ProgressBar(self.pb_start_x +5*self.pb_hd+30+40+30+40+30, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 72),
            # ProgressBar(self.pb_start_x +6*self.pb_hd+30+40+30+40+30+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 71),
            # ProgressBar(self.pb_start_x +7*self.pb_hd+30+40+30+40+30+50+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 70),
            # ProgressBar(self.pb_start_x +8*self.pb_hd+30+40+30+40+30+50+50+50, self.pb_start_y + self.pb_vd*28, 60, self.pb_start_h, 69),
            # ProgressBar(self.pb_start_x +9*self.pb_hd+30+40+30+40+30+50+50+50+60, self.pb_start_y + self.pb_vd*28, 60, self.pb_start_h, 68),
            # ProgressBar(self.pb_start_x+10*self.pb_hd+30+40+30+40+30+50+50+50+60+60, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 67),
            # ProgressBar(self.pb_start_x, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 77),
            # ProgressBar(self.pb_start_x +1*self.pb_hd+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 76),
            # ProgressBar(self.pb_start_x +2*self.pb_hd+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 75),
            # ProgressBar(self.pb_start_x +3*self.pb_hd+30+40+30, self.pb_start_y + self.pb_vd*28, 40, self.pb_start_h, 74),
            # ProgressBar(self.pb_start_x +4*self.pb_hd+30+40+30+40, self.pb_start_y + self.pb_vd*28, 30, self.pb_start_h, 73),
            # ProgressBar(self.pb_start_x +5*self.pb_hd+30+40+30+40+30, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 72),
            # ProgressBar(self.pb_start_x +6*self.pb_hd+30+40+30+40+30+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 71),
            # ProgressBar(self.pb_start_x +7*self.pb_hd+30+40+30+40+30+50+50, self.pb_start_y + self.pb_vd*28, 50, self.pb_start_h, 70),
        ]


        drawingarea_progress_bar = Gtk.DrawingArea()
        drawingarea_progress_bar.connect("draw", self.on_draw_progress_bar)
        drawingarea_progress_bar.connect("button-press-event", self.on_click_progress_bar)  # Conectando o evento de clique
        drawingarea_progress_bar.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        stack.add_titled(drawingarea_progress_bar, "bar", "Bar")

        ## Matrix Tab with DrawingArea
        self.rects_per_col  = 19
        self.rects_per_line = 6
        self.rectangles_matrix = []
        drawingarea_matrix = Gtk.DrawingArea()
        drawingarea_matrix.connect("draw", self.on_draw_matrix)
        drawingarea_matrix.connect("button-press-event", self.on_click_matrix)  # Conectando o evento de clique
        drawingarea_matrix.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        stack.add_titled(drawingarea_matrix, "matrix", "Matrix")

        self.refresh_rectangles()



        # List Tab
        checkbutton_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        # label = Gtk.Label(label="Memorized Chapters:")
        # checkbutton_container.pack_start(label, False, False, 0)
        self.checkboxes = []
        for c in list_obj_chapter:
            checkbutton = Gtk.CheckButton(label=f"{c.number}. ({c.name_latin}) {c.name_arabic}")
            if c.number in user.mem_chapters:
                checkbutton.set_active(True)
            self.checkboxes.append((checkbutton, c))
            checkbutton.connect("toggled", lambda btn, obj=c: self.on_checkbox_toggled(btn, obj))
            checkbutton_container.pack_start(checkbutton, False, False, 0)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(checkbutton_container)
        stack.add_titled(scrolled_window, "list", "List")


        # Stats Tab
        self.label_stats = Gtk.Label()
        self.refresh_stats_label()
        stack.add_titled(self.label_stats, "stats", "Stats")


        # Profile Tab
        # label_profile = Gtk.Label()
        # label_profile.set_markup(
        #     f"<b>Username:</b> {user.username}\n"

        #     # '<a href="https://github.com/omarelladen" '
        #     # 'title="Visit website">GitHub</a>'
        # )
        # stack.add_titled(label_profile, "profile", "Profile")




        ## Stack Switcher
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        stack_switcher.set_halign(Gtk.Align.CENTER)  # horizontal
        # stack_switcher.set_valign(Gtk.Align.CENTER)  # vertical (optional)

        outerbox.pack_start(stack_switcher, False, True, 0)
        outerbox.pack_start(stack, True, True, 0)




    def on_draw_progress_bar(self, widget, cr):
        for rect in self.rectangles_progress_bar:
            cr.set_source_rgb(*rect.color)
            cr.rectangle(rect.x, rect.y, rect.width, rect.height)
            cr.fill()


    def on_click_progress_bar(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == Gdk.BUTTON_PRIMARY:
                for rect in self.rectangles_progress_bar:
                    if (rect.x <= event.x <= rect.x + rect.width and
                        rect.y <= event.y <= rect.y + rect.height):
                        print(f"Chapter {rect.chapter}")
                        # self.toggle_progress_bar(rect)
                        break



    def on_click_matrix(self, widget, event):
        # if event.type == Gdk.EventType.DOUBLE_BUTTON_PRESS: # Gdk.EventType._2BUTTON_PRESS
        #     pass
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == Gdk.BUTTON_PRIMARY:
                x, y = event.x, event.y
                for idx, (rx, ry, width, height, r, g, b) in enumerate(self.rectangles_matrix):
                    if rx <= x <= rx + width and ry <= y <= ry + height:
                        #self.toggle_rectangle(idx)
                        print(f"Chapter {idx+1}")
                        break
    def toggle_rectangle(self, idx):
        x, y, width, height, r, g, b = self.rectangles_matrix[idx]
        # Toggle colors
        if (r, g, b) == self.on_color:
            self.rectangles_matrix[idx] = (x, y, width, height, self.off_color)
        else:
            self.rectangles_matrix[idx] = (x, y, width, height, self.on_color)
        self.queue_draw()  # Redraw

    def on_draw_matrix(self, widget, cr):
        for x, y, width, height, r, g, b in self.rectangles_matrix:
            cr.set_source_rgb(r, g, b)
            cr.rectangle(x, y, width, height)
            cr.fill()

    def on_about_clicked(self, widget):
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

    def refresh_rectangles(self):
        # Update rectangle colors based on  by creating a new list
        self.rectangles_matrix = []
        for i in range(self.rects_per_col):
            for j in range(self.rects_per_line):
                x = 155+ (self.rects_per_line-1-j) * 35 # from left to right
                y = 15 + i * 20
                chapter_num = i * (self.rects_per_line) + j + 1
                r, g, b = self.off_color if chapter_num in user.mem_chapters else self.on_color
                self.rectangles_matrix.append((x, y, 30, 10, r, g, b))
        
        for rect in self.rectangles_progress_bar:
            rect.color = self.off_color if rect.chapter in user.mem_chapters else self.on_color

        self.queue_draw() # Redraw the matrix tab

    def on_checkbox_toggled(self, button, c=''):
        if button.get_active():
            user.mem_chapters.append(c.number)
            user.n_mem_chapters += 1
            user.n_mem_verses   += c.n_verses
            user.n_mem_words    += c.n_words
            user.n_mem_letters  += c.n_letters
            self.save_mem_chapters(c, 'add')
        else:
            user.mem_chapters.remove(c.number)
            user.n_mem_chapters -= 1
            user.n_mem_verses   -= c.n_verses
            user.n_mem_words    -= c.n_words
            user.n_mem_letters  -= c.n_letters
            self.save_mem_chapters(c, 'rm')
        self.refresh_stats_label()
        self.refresh_rectangles()

    def refresh_stats_label(self):
        self.label_stats.set_markup(
            f"<big><b>Username:</b> {user.username}</big>\n\n"
            f"<big><b>Chapters:</b> {user.n_mem_chapters} ({user.calc_pct_mem_chapters()}%)</big>\n"
            f"<big><b>Verses:</b> {user.n_mem_verses} ({user.calc_pct_mem_verses()}%)</big>\n"
            f"<big><b>Words:</b> {user.n_mem_words} ({user.calc_pct_mem_words()}%)</big>\n"
            f"<big><b>Letters:</b> {user.n_mem_letters} ({user.calc_pct_mem_letters()}%)</big>"
        )
    
    def save_mem_chapters(self, c, op):
        con = sqlite3.connect(dbfile)
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
            """, (user.username, c.number))
        elif op == 'rm':
            cur.execute("""
                DELETE FROM mem_chapters
                WHERE users_username = ? AND
                      chapters_number = ?
            """, (user.username, c.number))

        con.commit()
        con.close()



def load_db_data():
    con = sqlite3.connect(dbfile)
    cur = con.cursor()

    # Load persistance data from db
    table_book = [a for a in cur.execute("SELECT * FROM books")]
    list_obj_book=[]
    for b in table_book:
        list_obj_book.append(Book(b[1], b[2], b[3], b[4], b[5], b[6]))

    table_chapter = [a for a in cur.execute("SELECT * FROM chapters")]
    list_obj_chapter=[]
    for c in table_chapter:
        list_obj_chapter.append(Chapter(c[0], c[1], c[2], c[3], c[4], c[5]))

    table_user = [a for a in cur.execute("SELECT * FROM users")]
    if len(table_user) > 0:
        list_obj_user =[]
        for u in table_user:
            list_obj_user.append(User(u[0], u[1], u[2], u[3], u[4]))
        user = list_obj_user[0]

        table_user_mem_chapters = [a for a in cur.execute("SELECT * FROM mem_chapters")]
        for t in table_user_mem_chapters:
            user.mem_chapters.append(t[1])
    else:
        username = os.getlogin()
        user = User(username)

        cur.execute("""
            INSERT INTO users
            (username, n_mem_chapters, n_mem_words, n_mem_verses, n_mem_letters) VALUES (?, ?, ?, ?, ?)
            """, (user.username, user.n_mem_chapters, user.n_mem_words, user.n_mem_verses, user.n_mem_letters))
    
    con.commit()
    con.close()

    return user, list_obj_book, list_obj_chapter

if __name__ == '__main__':

    user, list_obj_book, list_obj_chapter = load_db_data()
    book = list_obj_book[0]

    # Load GTK Window
    win = GTKHafizWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

