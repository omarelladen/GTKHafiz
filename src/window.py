import os

import gi
from gi.repository import Gtk, Gio, Gdk, GdkPixbuf

from rectangle import Rectangle

class Window(Gtk.Window):
    def __init__(self, icon_file, db_manager, user, book, list_chapters):
        super().__init__()

        # Data
        self.db_manager = db_manager
        self.user = user
        self.book = book
        self.list_chapters = list_chapters

        # Icon
        self.icon_path = icon_file
        try:
            self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.icon_path, 64, 64, True)
            self.set_icon(self.pixbuf)
        except:
            print(f'Failed to load icon from "{self.icon_path}"')

        # Window
        self.win_default_l = 350
        self.win_default_h = 400
        self.set_border_width(6)
        self.set_default_size(self.win_default_l, self.win_default_h)
        self.set_size_request(580, 550)
        # self.set_resizable(False)

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
        pb_start_x = 14
        pb_start_y = 20
        pb_start_h = 10
        pb_vd = pb_start_h + 2
        pb_hd = 1

        scale = 500

        t_1 = 298
        s_1 = round(scale/t_1, 2)
        r_1 = 7 * s_1
        r_2_1 = 291 * s_1

        t_2 = 300
        s_2 = round(scale/t_2, 2)
        r_2_2 = 300 * s_2

        t_3 = 299.5
        s_3 = round(scale/t_3, 2)
        r_2_3 = 120 * s_3
        r_3_1 = 179.5 * s_3

        t_4 = 296.5
        s_4 = round(scale/t_4, 2)
        r_3_2 = 222.5 * s_4
        r_4_1 = 74 * s_4

        t_5 = 300
        s_5 = round(scale/t_5, 2)
        r_4_2 = 300 * s_5

        t_6 = 291.5
        s_6 = round(scale/t_6, 2)
        r_4_3 = 65 * s_6
        r_5_1 = 226.5 * s_6

        t_7 = 304.5
        s_7 = round(scale/t_7, 2)
        r_5_2 = 96.5 * s_7
        r_6_1 = 208 * s_7

        t_8 = 298
        s_8 = round(scale/t_8, 2)
        r_6_2 = 135 * s_8
        r_7_1 = 163 * s_8

        t_9 = 298
        s_9 = round(scale/t_9, 2)
        r_7_2 = 225 * s_9
        r_8_1 = 73 * s_9

        t_10 = 296.5
        s_10 = round(scale/t_10, 2)
        r_8_2 = 75 * s_10
        r_9_1 = 221.5 * s_10

        t_11 = 298.5
        s_11 = round(scale/t_11, 2)
        r_9_2 = 91.5 * s_11
        r_10 = 200 * s_11
        r_11_1 = 7 * s_11

        t_12 = 298
        s_12 = round(scale/t_12, 2)
        r_11_2 = 203 * s_12
        r_12_1 = 95 * s_12

        t_13 = 296
        s_13 = round(scale/t_13, 2)
        r_12_2 = 105 * s_13
        r_13 = 90 * s_13
        r_14 = 101 * s_13

        t_14 = 296
        s_14 = round(scale/t_14, 2)
        r_15 = 79 * s_14
        r_16 = 217 * s_14

        t_15 = 296
        s_15 = round(scale/t_15, 2)
        r_17 = 172 * s_15
        r_18_1 = 124 * s_15

        t_16 = 296
        s_16 = round(scale/t_16, 2)
        r_18_2 = 45 * s_16
        r_19 = 107 * s_16
        r_20 = 144 * s_16

        t_17 = 295
        s_17 = round(scale/t_17, 2)
        r_21 = 147 * s_17
        r_22 = 148 * s_17

        t_18 = 295
        s_18 = round(scale/t_18, 2)
        r_23 = 118 * s_18
        r_24 = 144 * s_18
        r_25_1 = 33 * s_18

        t_19 = 296
        s_19 = round(scale/t_19, 2)
        r_25_2 = 74 * s_19
        r_26 = 148 * s_19
        r_27_1 = 74 * s_19

        t_20 = 296
        s_20 = round(scale/t_20, 2)
        r_27_2 = 52 * s_20
        r_28 = 163 * s_20
        r_29_1 = 81 * s_20

        t_21 = 292
        s_21 = round(scale/t_21, 2)
        r_29_2 = 39 * s_21
        r_30 = 94 * s_21
        r_31 = 57 * s_21
        r_32 = 43 * s_21
        r_33_1 = 59 * s_21

        t_22 = 294
        s_22 = round(scale/t_22, 2)
        r_33_2 = 90 * s_22
        r_34 = 95 * s_22
        r_35 = 84 * s_22
        r_36_1 = 25 * s_22

        t_23 = 294
        s_23 = round(scale/t_23, 2)
        r_36_2 = 59 * s_23
        r_37 = 103 * s_23
        r_38 = 77 * s_23
        r_39_1 = 55 * s_23

        t_24 = 296
        s_24 = round(scale/t_24, 2)
        r_39_2 = 77 * s_24
        r_40 = 146 * s_24
        r_41_1 = 73 * s_24

        t_25 = 298
        s_25 = round(scale/t_25, 2)
        r_41_2 = 15 * s_25
        r_42 = 92 * s_25
        r_43 = 99 * s_25
        r_44 = 42 * s_25
        r_45 = 50 * s_25

        t_26 = 282
        s_26 = round(scale/t_26, 2)
        r_46 = 66 * s_26
        r_47 = 59 * s_26
        r_48 = 64 * s_26
        r_49 = 37 * s_26
        r_50 = 39 * s_26
        r_51_1 = 17 * s_26

        t_27 = 288
        s_27 = round(scale/t_27, 2)
        r_51_2 = 22 * s_27
        r_52 = 35 * s_27
        r_53 = 38 * s_27
        r_54 = 38 * s_27
        r_55 = 45 * s_27
        r_56 = 47 * s_27
        r_57 = 63 * s_27

        t_28 = 282
        s_28 = round(scale/t_28, 2)
        r_58 = 49 * s_28
        r_59 = 51 * s_28
        r_60 = 35 * s_28
        r_61 = 22 * s_28
        r_62 = 19 * s_28
        r_63 = 21 * s_28
        r_64 = 28 * s_28
        r_65 = 29 * s_28
        r_66 = 28 * s_28

        t_29 = 278
        s_29 = round(scale/t_29, 2)
        r_67 = 33 * s_29
        r_68 = 32 * s_29
        r_69 = 27 * s_29
        r_70 = 24 * s_29
        r_71 = 24 * s_29
        r_72 = 28 * s_29
        r_73 = 20 * s_29
        r_74 = 26 * s_29
        r_75 = 17 * s_29
        r_76 = 25 * s_29
        r_77 = 22 * s_29

        t_30 = 271
        s_30 = round(scale/t_30, 2)
        r_78 = 20 * s_30
        r_79 = 20 * s_30
        r_80 = 15 * s_30
        r_81 = 12 * s_30
        r_82 = 9 * s_30
        r_83 = 19 * s_30
        r_84 = 12 * s_30
        r_85 = 12 * s_30
        r_86 = 7 * s_30
        r_87 = 8 * s_30
        r_88 = 11 * s_30
        r_89 = 16 * s_30
        r_90 = 9 * s_30
        r_91 = 7 * s_30
        r_92 = 8 * s_30
        r_93 = 5 * s_30
        r_94 = 3 * s_30
        r_95 = 4 * s_30
        r_96 = 8 * s_30
        r_97 = 3 * s_30
        r_98 = 10 * s_30
        r_99 = 4 * s_30
        r_100 = 5 * s_30
        r_101 = 5 * s_30
        r_102 = 3 * s_30
        r_103 = 2 * s_30
        r_104 = 4 * s_30
        r_105 = 3 * s_30
        r_106 = 3 * s_30
        r_107 = 4 * s_30
        r_108 = 2 * s_30
        r_109 = 3 * s_30
        r_110 = 3 * s_30
        r_111 = 3 * s_30
        r_112 = 2 * s_30
        r_113 = 3 * s_30
        r_114 = 4 * s_30

        self.list_rect_progress_bar = []
        self.list_rect_progress_bar.append(Rectangle(0, 0 + pb_start_y + pb_vd*0, 0, 0, "Juz'"))

        self.list_rect_progress_bar.append(Rectangle(pb_start_x/4, pb_start_h+pb_start_y + pb_vd*0, 0, 0, "Juz 1"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y+pb_vd*0, r_2_1, pb_start_h, 2)); acum += r_2_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y+pb_vd*0, r_1, pb_start_h, 1))

        self.list_rect_progress_bar.append(Rectangle(pb_start_x/4, pb_start_h + pb_start_y + pb_vd*1, 0, 0, "Juz 2"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*1, r_2_2, pb_start_h, 2))

        self.list_rect_progress_bar.append(Rectangle(pb_start_x/4, pb_start_h + pb_start_y + pb_vd*2, 0, 0, "Juz 3"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*2, r_3_1, pb_start_h, 3)); acum += r_3_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*2, r_2_3, pb_start_h, 2))

        self.list_rect_progress_bar.append(Rectangle(pb_start_x/4, pb_start_h + pb_start_y + pb_vd*3, 0, 0, "Juz 4"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*3, r_4_1, pb_start_h, 4)); acum += r_4_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*3, r_3_2, pb_start_h, 3))

        self.list_rect_progress_bar.append(Rectangle(pb_start_x/4, pb_start_h + pb_start_y + pb_vd*4, 0, 0, "Juz 5"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*4, r_4_2, pb_start_h, 4))

        self.list_rect_progress_bar.append(Rectangle(pb_start_x/4, pb_start_h + pb_start_y + pb_vd*5, 0, 0, "Juz 6"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*5, r_5_1, pb_start_h, 5)); acum += r_5_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*5, r_4_3, pb_start_h, 4))

        self.list_rect_progress_bar.append(Rectangle(pb_start_x/4, pb_start_h + pb_start_y + pb_vd*6, 0, 0, "Juz 7"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*6, r_6_1, pb_start_h, 6)); acum += r_6_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*6, r_5_2, pb_start_h, 5))

        self.list_rect_progress_bar.append(Rectangle(pb_start_x/4, pb_start_h + pb_start_y + pb_vd*7, 0, 0, "Juz 8"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*7, r_7_1, pb_start_h, 7)); acum += r_7_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*7, r_6_2, pb_start_h, 6))

        self.list_rect_progress_bar.append(Rectangle(pb_start_x/4, pb_start_h + pb_start_y + pb_vd*8, 0, 0, "Juz 9"),)
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*8, r_8_1, pb_start_h, 8)); acum += r_8_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*8, r_7_2, pb_start_h, 7))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*9, 0, 0, "Juz 10"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*9, r_9_1, pb_start_h, 9)); acum += r_9_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*9, r_8_2, pb_start_h, 8))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*10, 0, 0, "Juz 11"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*10, r_11_1, pb_start_h, 11)); acum += r_11_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*10, r_10, pb_start_h, 10)); acum += r_10
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*10, r_9_2, pb_start_h, 9))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*11, 0, 0, "Juz 12"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(pb_start_x, pb_start_y + pb_vd*11, r_12_1, pb_start_h, 12))
        self.list_rect_progress_bar.append(Rectangle(pb_start_x+1*pb_hd+r_12_1, pb_start_y + pb_vd*11, r_11_2, pb_start_h, 11))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*12, 0, 0, "Juz 13"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*12, r_14, pb_start_h, 14)); acum += r_14
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*12, r_13, pb_start_h, 13)); acum += r_13
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*12, r_12_2, pb_start_h, 12))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*13, 0, 0, "Juz 14"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*13, r_16, pb_start_h, 16)); acum += r_16
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*13, r_15, pb_start_h, 15))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*14, 0, 0, "Juz 15"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*14, r_18_1, pb_start_h, 18)); acum += r_18_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*14, r_17, pb_start_h, 17))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*15, 0, 0, "Juz 16"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*15, r_20, pb_start_h, 20)); acum += r_20
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*15, r_19, pb_start_h, 19)); acum += r_19
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*15, r_18_2, pb_start_h, 18))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*16, 0, 0, "Juz 17"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*16, r_22, pb_start_h, 22)); acum += r_22
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*16, r_21, pb_start_h, 21))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*17, 0, 0, "Juz 18"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*17, r_25_1, pb_start_h, 25)); acum += r_25_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*17, r_24, pb_start_h, 24)); acum += r_24
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*17, r_23, pb_start_h, 23))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*18, 0, 0, "Juz 19"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*18, r_27_1, pb_start_h, 27)); acum += r_27_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*18, r_26, pb_start_h, 26)); acum += r_26
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*18, r_25_2, pb_start_h, 25))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*19, 0, 0, "Juz 20"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*19, r_29_1, pb_start_h, 29)); acum += r_29_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*19, r_28, pb_start_h, 28)); acum += r_28
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*19, r_27_2, pb_start_h, 27))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*20, 0, 0, "Juz 21"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*20, r_33_1, pb_start_h, 33)); acum += r_33_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*20, r_32, pb_start_h, 32)); acum += r_32
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*20, r_31, pb_start_h, 31)); acum += r_31
        self.list_rect_progress_bar.append(Rectangle(3*pb_hd+acum, pb_start_y + pb_vd*20, r_30, pb_start_h, 30)); acum += r_30
        self.list_rect_progress_bar.append(Rectangle(4*pb_hd+acum, pb_start_y + pb_vd*20, r_29_2, pb_start_h, 29))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*21, 0, 0, "Juz 22"),)
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*21, r_36_1, pb_start_h, 36)); acum += r_36_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*21, r_35, pb_start_h, 35)); acum += r_35
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*21, r_34, pb_start_h, 34)); acum += r_34
        self.list_rect_progress_bar.append(Rectangle(3*pb_hd+acum, pb_start_y + pb_vd*21, r_33_2, pb_start_h, 33))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*22, 0, 0, "Juz 23"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*22, r_39_1, pb_start_h, 39)); acum += r_39_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*22, r_38, pb_start_h, 38)); acum += r_38
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*22, r_37, pb_start_h, 37)); acum += r_37
        self.list_rect_progress_bar.append(Rectangle(3*pb_hd+acum, pb_start_y + pb_vd*22, r_36_2, pb_start_h, 36))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*23, 0, 0, "Juz 24"),)
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*23, r_41_1, pb_start_h, 41)); acum += r_41_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*23, r_40, pb_start_h, 40)); acum += r_40
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*23, r_39_2, pb_start_h, 39))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*24, 0, 0, "Juz 25"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*24, r_45, pb_start_h, 45)); acum += r_45
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*24, r_44, pb_start_h, 44)); acum += r_44
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*24, r_43, pb_start_h, 43)); acum += r_43
        self.list_rect_progress_bar.append(Rectangle(3*pb_hd+acum, pb_start_y + pb_vd*24, r_42, pb_start_h, 42)); acum += r_42
        self.list_rect_progress_bar.append(Rectangle(4*pb_hd+acum, pb_start_y + pb_vd*24, r_41_2, pb_start_h, 41))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*25, 0, 0, "Juz 26"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*25, r_51_1, pb_start_h, 51)); acum += r_51_1
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*25, r_50, pb_start_h, 50)); acum += r_50
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*25, r_49, pb_start_h, 49)); acum += r_49
        self.list_rect_progress_bar.append(Rectangle(3*pb_hd+acum, pb_start_y + pb_vd*25, r_48, pb_start_h, 48)); acum += r_48
        self.list_rect_progress_bar.append(Rectangle(4*pb_hd+acum, pb_start_y + pb_vd*25, r_47, pb_start_h, 47)); acum += r_47
        self.list_rect_progress_bar.append(Rectangle(5*pb_hd+acum, pb_start_y + pb_vd*25, r_46, pb_start_h, 46))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*26, 0, 0, "Juz 27"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*26, r_57, pb_start_h, 57)); acum += r_57
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*26, r_56, pb_start_h, 56)); acum += r_56
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*26, r_55, pb_start_h, 55)); acum += r_55
        self.list_rect_progress_bar.append(Rectangle(3*pb_hd+acum, pb_start_y + pb_vd*26, r_54, pb_start_h, 54)); acum += r_54
        self.list_rect_progress_bar.append(Rectangle(4*pb_hd+acum, pb_start_y + pb_vd*26, r_53, pb_start_h, 53)); acum += r_53
        self.list_rect_progress_bar.append(Rectangle(5*pb_hd+acum, pb_start_y + pb_vd*26, r_52, pb_start_h, 52)); acum += r_52
        self.list_rect_progress_bar.append(Rectangle(6*pb_hd+acum, pb_start_y + pb_vd*26, r_51_2, pb_start_h, 51))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*27, 0, 0, "Juz 28"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle(0*pb_hd+acum, pb_start_y + pb_vd*27, r_66, pb_start_h, 66)); acum += r_66
        self.list_rect_progress_bar.append(Rectangle(1*pb_hd+acum, pb_start_y + pb_vd*27, r_65, pb_start_h, 65)); acum += r_65
        self.list_rect_progress_bar.append(Rectangle(2*pb_hd+acum, pb_start_y + pb_vd*27, r_64, pb_start_h, 64)); acum += r_64
        self.list_rect_progress_bar.append(Rectangle(3*pb_hd+acum, pb_start_y + pb_vd*27, r_63, pb_start_h, 63)); acum += r_63
        self.list_rect_progress_bar.append(Rectangle(4*pb_hd+acum, pb_start_y + pb_vd*27, r_62, pb_start_h, 62)); acum += r_62
        self.list_rect_progress_bar.append(Rectangle(5*pb_hd+acum, pb_start_y + pb_vd*27, r_61, pb_start_h, 61)); acum += r_61
        self.list_rect_progress_bar.append(Rectangle(6*pb_hd+acum, pb_start_y + pb_vd*27, r_60, pb_start_h, 60)); acum += r_60
        self.list_rect_progress_bar.append(Rectangle(7*pb_hd+acum, pb_start_y + pb_vd*27, r_59, pb_start_h, 59)); acum += r_59
        self.list_rect_progress_bar.append(Rectangle(8*pb_hd+acum, pb_start_y + pb_vd*27, r_58, pb_start_h, 58))

        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*28, 0, 0, "Juz 29"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle( 0*pb_hd+acum, pb_start_y + pb_vd*28, r_77, pb_start_h, 77)); acum += r_77
        self.list_rect_progress_bar.append(Rectangle( 1*pb_hd+acum, pb_start_y + pb_vd*28, r_76, pb_start_h, 76)); acum += r_76
        self.list_rect_progress_bar.append(Rectangle( 2*pb_hd+acum, pb_start_y + pb_vd*28, r_75, pb_start_h, 75)); acum += r_75
        self.list_rect_progress_bar.append(Rectangle( 3*pb_hd+acum, pb_start_y + pb_vd*28, r_74, pb_start_h, 74)); acum += r_74
        self.list_rect_progress_bar.append(Rectangle( 4*pb_hd+acum, pb_start_y + pb_vd*28, r_73, pb_start_h, 73)); acum += r_73
        self.list_rect_progress_bar.append(Rectangle( 5*pb_hd+acum, pb_start_y + pb_vd*28, r_72, pb_start_h, 72)); acum += r_72
        self.list_rect_progress_bar.append(Rectangle( 6*pb_hd+acum, pb_start_y + pb_vd*28, r_71, pb_start_h, 71)); acum += r_71
        self.list_rect_progress_bar.append(Rectangle( 7*pb_hd+acum, pb_start_y + pb_vd*28, r_70, pb_start_h, 70)); acum += r_70
        self.list_rect_progress_bar.append(Rectangle( 8*pb_hd+acum, pb_start_y + pb_vd*28, r_69, pb_start_h, 69)); acum += r_69
        self.list_rect_progress_bar.append(Rectangle( 9*pb_hd+acum, pb_start_y + pb_vd*28, r_68, pb_start_h, 68)); acum += r_68
        self.list_rect_progress_bar.append(Rectangle(10*pb_hd+acum, pb_start_y + pb_vd*28, r_67, pb_start_h, 67))


        self.list_rect_progress_bar.append(Rectangle(0, pb_start_h + pb_start_y + pb_vd*29, 0, 0, "Juz 30"))
        acum = pb_start_x
        self.list_rect_progress_bar.append(Rectangle( 0*pb_hd+acum, pb_start_y + pb_vd*29, r_114, pb_start_h, 114)); acum += r_114
        self.list_rect_progress_bar.append(Rectangle( 1*pb_hd+acum, pb_start_y + pb_vd*29, r_113, pb_start_h, 113)); acum += r_113
        self.list_rect_progress_bar.append(Rectangle( 2*pb_hd+acum, pb_start_y + pb_vd*29, r_112, pb_start_h, 112)); acum += r_112
        self.list_rect_progress_bar.append(Rectangle( 3*pb_hd+acum, pb_start_y + pb_vd*29, r_111, pb_start_h, 111)); acum += r_111
        self.list_rect_progress_bar.append(Rectangle( 4*pb_hd+acum, pb_start_y + pb_vd*29, r_110, pb_start_h, 110)); acum += r_110
        self.list_rect_progress_bar.append(Rectangle( 5*pb_hd+acum, pb_start_y + pb_vd*29, r_109, pb_start_h, 109)); acum += r_109
        self.list_rect_progress_bar.append(Rectangle( 6*pb_hd+acum, pb_start_y + pb_vd*29, r_108, pb_start_h, 108)); acum += r_108
        self.list_rect_progress_bar.append(Rectangle( 7*pb_hd+acum, pb_start_y + pb_vd*29, r_107, pb_start_h, 107)); acum += r_107
        self.list_rect_progress_bar.append(Rectangle( 8*pb_hd+acum, pb_start_y + pb_vd*29, r_106, pb_start_h, 106)); acum += r_106
        self.list_rect_progress_bar.append(Rectangle( 9*pb_hd+acum, pb_start_y + pb_vd*29, r_105, pb_start_h, 105)); acum += r_106
        self.list_rect_progress_bar.append(Rectangle(10*pb_hd+acum, pb_start_y + pb_vd*29, r_104, pb_start_h, 104)); acum += r_104
        self.list_rect_progress_bar.append(Rectangle(11*pb_hd+acum, pb_start_y + pb_vd*29, r_103, pb_start_h, 103)); acum += r_103
        self.list_rect_progress_bar.append(Rectangle(12*pb_hd+acum, pb_start_y + pb_vd*29, r_102, pb_start_h, 102)); acum += r_102
        self.list_rect_progress_bar.append(Rectangle(13*pb_hd+acum, pb_start_y + pb_vd*29, r_101, pb_start_h, 101)); acum += r_101
        self.list_rect_progress_bar.append(Rectangle(14*pb_hd+acum, pb_start_y + pb_vd*29, r_100, pb_start_h, 100)); acum += r_100
        self.list_rect_progress_bar.append(Rectangle(15*pb_hd+acum, pb_start_y + pb_vd*29, r_99,  pb_start_h, 99)); acum += r_99
        self.list_rect_progress_bar.append(Rectangle(16*pb_hd+acum, pb_start_y + pb_vd*29, r_98,  pb_start_h, 98)); acum += r_98
        self.list_rect_progress_bar.append(Rectangle(17*pb_hd+acum, pb_start_y + pb_vd*29, r_97,  pb_start_h, 97)); acum += r_97
        self.list_rect_progress_bar.append(Rectangle(18*pb_hd+acum, pb_start_y + pb_vd*29, r_96,  pb_start_h, 96)); acum += r_96
        self.list_rect_progress_bar.append(Rectangle(19*pb_hd+acum, pb_start_y + pb_vd*29, r_95,  pb_start_h, 95)); acum += r_95
        self.list_rect_progress_bar.append(Rectangle(20*pb_hd+acum, pb_start_y + pb_vd*29, r_94,  pb_start_h, 94)); acum += r_94
        self.list_rect_progress_bar.append(Rectangle(21*pb_hd+acum, pb_start_y + pb_vd*29, r_93,  pb_start_h, 93)); acum += r_93
        self.list_rect_progress_bar.append(Rectangle(22*pb_hd+acum, pb_start_y + pb_vd*29, r_92,  pb_start_h, 92)); acum += r_92
        self.list_rect_progress_bar.append(Rectangle(23*pb_hd+acum, pb_start_y + pb_vd*29, r_91,  pb_start_h, 91)); acum += r_91
        self.list_rect_progress_bar.append(Rectangle(24*pb_hd+acum, pb_start_y + pb_vd*29, r_90,  pb_start_h, 90)); acum += r_90
        self.list_rect_progress_bar.append(Rectangle(25*pb_hd+acum, pb_start_y + pb_vd*29, r_89,  pb_start_h, 89)); acum += r_89
        self.list_rect_progress_bar.append(Rectangle(26*pb_hd+acum, pb_start_y + pb_vd*29, r_88,  pb_start_h, 88)); acum += r_88
        self.list_rect_progress_bar.append(Rectangle(27*pb_hd+acum, pb_start_y + pb_vd*29, r_87,  pb_start_h, 87)); acum += r_87
        self.list_rect_progress_bar.append(Rectangle(28*pb_hd+acum, pb_start_y + pb_vd*29, r_86,  pb_start_h, 86)); acum += r_86
        self.list_rect_progress_bar.append(Rectangle(29*pb_hd+acum, pb_start_y + pb_vd*29, r_85,  pb_start_h, 85)); acum += r_85
        self.list_rect_progress_bar.append(Rectangle(30*pb_hd+acum, pb_start_y + pb_vd*29, r_84,  pb_start_h, 84)); acum += r_84
        self.list_rect_progress_bar.append(Rectangle(31*pb_hd+acum, pb_start_y + pb_vd*29, r_83,  pb_start_h, 83)); acum += r_83
        self.list_rect_progress_bar.append(Rectangle(32*pb_hd+acum, pb_start_y + pb_vd*29, r_82,  pb_start_h, 82)); acum += r_82
        self.list_rect_progress_bar.append(Rectangle(33*pb_hd+acum, pb_start_y + pb_vd*29, r_81,  pb_start_h, 81)); acum += r_81
        self.list_rect_progress_bar.append(Rectangle(34*pb_hd+acum, pb_start_y + pb_vd*29, r_80,  pb_start_h, 80)); acum += r_80
        self.list_rect_progress_bar.append(Rectangle(35*pb_hd+acum, pb_start_y + pb_vd*29, r_79,  pb_start_h, 79)); acum += r_79
        self.list_rect_progress_bar.append(Rectangle(36*pb_hd+acum, pb_start_y + pb_vd*29, r_78,  pb_start_h, 78))


        # Progress Bar Tab
        drawingarea_progress_bar = Gtk.DrawingArea()
        drawingarea_progress_bar.connect("draw", self.on_draw_progress_bar)
        drawingarea_progress_bar.connect("button-press-event", self.on_click_progress_bar)
        drawingarea_progress_bar.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        stack.add_titled(drawingarea_progress_bar, "bars", "Bars")

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
        about.set_version("0.1.1")
        about.set_comments("Track Qur'an memorization visually")
        about.set_website("https://github.com/omarelladen/GTK-Hafiz")
        about.set_website_label("Repository")
        about.set_authors(["Omar El Laden"])
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_copyright("Copyright © 2025 Omar El Laden")

        try:
            about.set_logo(self.pixbuf)
        except:
            print(f'Failed to load icon from "{self.icon_path}"')

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

            # Juz' indication
            if isinstance(rect.caption, str) and "Juz" in rect.caption:
                cr.show_text(rect.caption.replace("Juz ", ""))

            cr.fill()


    def show_chapter_popover(self, rect, widget, event):
        self.label_chapter.set_text(f"{rect.caption}")
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
                self.list_rect_matrix.append(Rectangle(x, y, 30, 10, chapter_num, (r, g, b)))

        # Refresh Progress Bar Rectangles
        for rect in self.list_rect_progress_bar:
            rect.color = self.rect_off_color if rect.caption in self.user.mem_chapters else self.rect_on_color
        
        # Ensure Redraw
        self.queue_draw() 


    def refresh_stats_label(self):
        self.label_stats.set_markup(
            f"<big><b>Chapters:</b> {self.user.n_mem_chapters} ({round(self.user.n_mem_chapters / self.book.n_chapters * 100, 1)}%)</big>\n"
            f"<big><b>Verses:</b> {self.user.n_mem_verses} ({round(self.user.n_mem_verses / self.book.n_verses * 100, 1)}%)</big>\n"
            f"<big><b>Words:</b> {self.user.n_mem_words} ({round(self.user.n_mem_words / self.book.n_words * 100, 1)}%)</big>\n"
            f"<big><b>Letters:</b> {self.user.n_mem_letters} ({round(self.user.n_mem_letters / self.book.n_letters * 100, 1)}%)</big>"
        )
