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
        self.set_resizable(False)

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

        # Create Progress Bars Rectangles
        pb_line_x0 = 14 # initial x
        pb_line_y0 = 20 # initial y
        pb_height = 10 # bar height
        pb_lines_dist = pb_height + 2 # distance between lines
        pb_dist = 1 # distance between 2 bars
        pb_line_width = 500 # lenght of line

        t_1 = 298
        s_1 = pb_line_width/t_1
        r_1   = 7   * s_1
        r_2_1 = 291 * s_1

        t_2 = 300
        s_2 = pb_line_width/t_2
        r_2_2 = 300 * s_2

        t_3 = 299.5
        s_3 = pb_line_width/t_3
        r_2_3 = 120   * s_3
        r_3_1 = 179.5 * s_3

        t_4 = 296.5
        s_4 = pb_line_width/t_4
        r_3_2 = 222.5 * s_4
        r_4_1 = 74    * s_4

        t_5 = 300
        s_5 = pb_line_width/t_5
        r_4_2 = 300 * s_5

        t_6 = 291.5
        s_6 = pb_line_width/t_6
        r_4_3 = 65    * s_6
        r_5_1 = 226.5 * s_6

        t_7 = 304.5
        s_7 = pb_line_width/t_7
        r_5_2 = 96.5 * s_7
        r_6_1 = 208  * s_7

        t_8 = 298
        s_8 = pb_line_width/t_8
        r_6_2 = 135 * s_8
        r_7_1 = 163 * s_8

        t_9 = 298
        s_9 = pb_line_width/t_9
        r_7_2 = 225 * s_9
        r_8_1 = 73  * s_9

        t_10 = 296.5
        s_10 = pb_line_width/t_10
        r_8_2 = 75    * s_10
        r_9_1 = 221.5 * s_10

        t_11 = 298.5
        s_11 = pb_line_width/t_11
        r_9_2  = 91.5 * s_11
        r_10   = 200  * s_11
        r_11_1 = 7    * s_11

        t_12 = 298
        s_12 = pb_line_width/t_12
        r_11_2 = 203 * s_12
        r_12_1 = 95  * s_12

        t_13 = 296
        s_13 = pb_line_width/t_13
        r_12_2 = 105 * s_13
        r_13   = 90  * s_13
        r_14   = 101 * s_13

        t_14 = 296
        s_14 = pb_line_width/t_14
        r_15 = 79  * s_14
        r_16 = 217 * s_14

        t_15 = 296
        s_15 = pb_line_width/t_15
        r_17   = 172 * s_15
        r_18_1 = 124 * s_15

        t_16 = 296
        s_16 = pb_line_width/t_16
        r_18_2 = 45  * s_16
        r_19   = 107 * s_16
        r_20   = 144 * s_16

        t_17 = 295
        s_17 = pb_line_width/t_17
        r_21 = 147 * s_17
        r_22 = 148 * s_17

        t_18 = 295
        s_18 = pb_line_width/t_18
        r_23   = 118 * s_18
        r_24   = 144 * s_18
        r_25_1 = 33  * s_18

        t_19 = 296
        s_19 = pb_line_width/t_19
        r_25_2 = 74  * s_19
        r_26   = 148 * s_19
        r_27_1 = 74  * s_19

        t_20 = 296
        s_20 = pb_line_width/t_20
        r_27_2 = 52  * s_20
        r_28   = 163 * s_20
        r_29_1 = 81  * s_20

        t_21 = 292
        s_21 = pb_line_width/t_21
        r_29_2 = 39 * s_21
        r_30   = 94 * s_21
        r_31   = 57 * s_21
        r_32   = 43 * s_21
        r_33_1 = 59 * s_21

        t_22 = 294
        s_22 = pb_line_width/t_22
        r_33_2 = 90 * s_22
        r_34   = 95 * s_22
        r_35   = 84 * s_22
        r_36_1 = 25 * s_22

        t_23 = 294
        s_23 = pb_line_width/t_23
        r_36_2 = 59  * s_23
        r_37   = 103 * s_23
        r_38   = 77  * s_23
        r_39_1 = 55  * s_23

        t_24 = 296
        s_24 = pb_line_width/t_24
        r_39_2 = 77  * s_24
        r_40   = 146 * s_24
        r_41_1 = 73  * s_24

        t_25 = 298
        s_25 = pb_line_width/t_25
        r_41_2 = 15 * s_25
        r_42   = 92 * s_25
        r_43   = 99 * s_25
        r_44   = 42 * s_25
        r_45   = 50 * s_25

        t_26 = 282
        s_26 = pb_line_width/t_26
        r_46   = 66 * s_26
        r_47   = 59 * s_26
        r_48   = 64 * s_26
        r_49   = 37 * s_26
        r_50   = 39 * s_26
        r_51_1 = 17 * s_26

        t_27 = 288
        s_27 = pb_line_width/t_27
        r_51_2 = 22 * s_27
        r_52   = 35 * s_27
        r_53   = 38 * s_27
        r_54   = 38 * s_27
        r_55   = 45 * s_27
        r_56   = 47 * s_27
        r_57   = 63 * s_27

        t_28 = 282
        s_28 = pb_line_width/t_28
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
        s_29 = pb_line_width/t_29
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
        s_30 = pb_line_width/t_30
        r_78  = 20 * s_30
        r_79  = 20 * s_30
        r_80  = 15 * s_30
        r_81  = 12 * s_30
        r_82  = 9  * s_30
        r_83  = 19 * s_30
        r_84  = 12 * s_30
        r_85  = 12 * s_30
        r_86  = 7  * s_30
        r_87  = 8  * s_30
        r_88  = 11 * s_30
        r_89  = 16 * s_30
        r_90  = 9  * s_30
        r_91  = 7  * s_30
        r_92  = 8  * s_30
        r_93  = 5  * s_30
        r_94  = 3  * s_30
        r_95  = 4  * s_30
        r_96  = 8  * s_30
        r_97  = 3  * s_30
        r_98  = 10 * s_30
        r_99  = 4  * s_30
        r_100 = 5  * s_30
        r_101 = 5  * s_30
        r_102 = 3  * s_30
        r_103 = 2  * s_30
        r_104 = 4  * s_30
        r_105 = 3  * s_30
        r_106 = 3  * s_30
        r_107 = 4  * s_30
        r_108 = 2  * s_30
        r_109 = 3  * s_30
        r_110 = 3  * s_30
        r_111 = 3  * s_30
        r_112 = 2  * s_30
        r_113 = 3  * s_30
        r_114 = 4  * s_30


        self.list_rect_progress_bar = []
        self.list_rect_progress_bar.append(Rectangle(0, 0 + pb_line_y0 + pb_lines_dist*0, 0, 0, "Juz'"))

        self.list_rect_progress_bar.append(Rectangle(pb_line_x0/4, pb_height+pb_line_y0 + pb_lines_dist*0, 0, 0, "Juz 1"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0+pb_lines_dist*0, r_2_1-pb_dist, pb_height, 2)); pb_offset += r_2_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0+pb_lines_dist*0, r_1,         pb_height, 1))

        self.list_rect_progress_bar.append(Rectangle(pb_line_x0/4, pb_height + pb_line_y0 + pb_lines_dist*1, 0, 0, "Juz 2"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*1, r_2_2, pb_height, 2))

        self.list_rect_progress_bar.append(Rectangle(pb_line_x0/4, pb_height + pb_line_y0 + pb_lines_dist*2, 0, 0, "Juz 3"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*2, r_3_1-pb_dist, pb_height, 3)); pb_offset += r_3_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*2, r_2_3,       pb_height, 2))

        self.list_rect_progress_bar.append(Rectangle(pb_line_x0/4, pb_height + pb_line_y0 + pb_lines_dist*3, 0, 0, "Juz 4"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*3, r_4_1-pb_dist, pb_height, 4)); pb_offset += r_4_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*3, r_3_2,       pb_height, 3))

        self.list_rect_progress_bar.append(Rectangle(pb_line_x0/4, pb_height + pb_line_y0 + pb_lines_dist*4, 0, 0, "Juz 5"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*4, r_4_2, pb_height, 4))

        self.list_rect_progress_bar.append(Rectangle(pb_line_x0/4, pb_height + pb_line_y0 + pb_lines_dist*5, 0, 0, "Juz 6"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*5, r_5_1-pb_dist, pb_height, 5)); pb_offset += r_5_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*5, r_4_3, pb_height, 4))

        self.list_rect_progress_bar.append(Rectangle(pb_line_x0/4, pb_height + pb_line_y0 + pb_lines_dist*6, 0, 0, "Juz 7"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*6, r_6_1-pb_dist, pb_height, 6)); pb_offset += r_6_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*6, r_5_2,       pb_height, 5))

        self.list_rect_progress_bar.append(Rectangle(pb_line_x0/4, pb_height + pb_line_y0 + pb_lines_dist*7, 0, 0, "Juz 8"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*7, r_7_1-pb_dist, pb_height, 7)); pb_offset += r_7_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*7, r_6_2,       pb_height, 6))

        self.list_rect_progress_bar.append(Rectangle(pb_line_x0/4, pb_height + pb_line_y0 + pb_lines_dist*8, 0, 0, "Juz 9"),)
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*8, r_8_1-pb_dist, pb_height, 8)); pb_offset += r_8_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*8, r_7_2,       pb_height, 7))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*9, 0, 0, "Juz 10"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*9, r_9_1-pb_dist, pb_height, 9)); pb_offset += r_9_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*9, r_8_2,       pb_height, 8))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*10, 0, 0, "Juz 11"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*10, r_11_1-pb_dist, pb_height, 11)); pb_offset += r_11_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*10, r_10  -pb_dist, pb_height, 10)); pb_offset += r_10
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*10, r_9_2,        pb_height, 9))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*11, 0, 0, "Juz 12"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*11, r_12_1-pb_dist, pb_height, 12)); pb_offset += r_12_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*11, r_11_2, pb_height, 11))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*12, 0, 0, "Juz 13"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*12, r_14-pb_dist, pb_height, 14)); pb_offset += r_14
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*12, r_13-pb_dist, pb_height, 13)); pb_offset += r_13
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*12, r_12_2,     pb_height, 12))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*13, 0, 0, "Juz 14"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*13, r_16-pb_dist, pb_height, 16)); pb_offset += r_16
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*13, r_15,       pb_height, 15))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*14, 0, 0, "Juz 15"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*14, r_18_1-pb_dist, pb_height, 18)); pb_offset += r_18_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*14, r_17,         pb_height, 17))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*15, 0, 0, "Juz 16"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*15, r_20-pb_dist, pb_height, 20)); pb_offset += r_20
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*15, r_19-pb_dist, pb_height, 19)); pb_offset += r_19
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*15, r_18_2,     pb_height, 18))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*16, 0, 0, "Juz 17"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*16, r_22, pb_height, 22)); pb_offset += r_22
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*16, r_21, pb_height, 21))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*17, 0, 0, "Juz 18"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*17, r_25_1-pb_dist, pb_height, 25)); pb_offset += r_25_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*17, r_24  -pb_dist, pb_height, 24)); pb_offset += r_24
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*17, r_23,         pb_height, 23))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*18, 0, 0, "Juz 19"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*18, r_27_1-pb_dist, pb_height, 27)); pb_offset += r_27_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*18, r_26  -pb_dist, pb_height, 26)); pb_offset += r_26
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*18, r_25_2,       pb_height, 25))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*19, 0, 0, "Juz 20"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*19, r_29_1-pb_dist, pb_height, 29)); pb_offset += r_29_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*19, r_28  -pb_dist, pb_height, 28)); pb_offset += r_28
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*19, r_27_2,       pb_height, 27))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*20, 0, 0, "Juz 21"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*20, r_33_1-pb_dist, pb_height, 33)); pb_offset += r_33_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*20, r_32  -pb_dist, pb_height, 32)); pb_offset += r_32
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*20, r_31  -pb_dist, pb_height, 31)); pb_offset += r_31
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*20, r_30  -pb_dist, pb_height, 30)); pb_offset += r_30
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*20, r_29_2,       pb_height, 29))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*21, 0, 0, "Juz 22"),)
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*21, r_36_1-pb_dist, pb_height, 36)); pb_offset += r_36_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*21, r_35  -pb_dist, pb_height, 35)); pb_offset += r_35
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*21, r_34  -pb_dist, pb_height, 34)); pb_offset += r_34
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*21, r_33_2,       pb_height, 33))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*22, 0, 0, "Juz 23"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*22, r_39_1-pb_dist, pb_height, 39)); pb_offset += r_39_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*22, r_38  -pb_dist, pb_height, 38)); pb_offset += r_38
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*22, r_37  -pb_dist, pb_height, 37)); pb_offset += r_37
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*22, r_36_2,       pb_height, 36))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*23, 0, 0, "Juz 24"),)
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*23, r_41_1-pb_dist, pb_height, 41)); pb_offset += r_41_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*23, r_40  -pb_dist, pb_height, 40)); pb_offset += r_40
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*23, r_39_2,       pb_height, 39))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*24, 0, 0, "Juz 25"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*24, r_45-pb_dist, pb_height, 45)); pb_offset += r_45
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*24, r_44-pb_dist, pb_height, 44)); pb_offset += r_44
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*24, r_43-pb_dist, pb_height, 43)); pb_offset += r_43
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*24, r_42-pb_dist, pb_height, 42)); pb_offset += r_42
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*24, r_41_2,     pb_height, 41))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*25, 0, 0, "Juz 26"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*25, r_51_1-pb_dist, pb_height, 51)); pb_offset += r_51_1
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*25, r_50  -pb_dist, pb_height, 50)); pb_offset += r_50
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*25, r_49  -pb_dist, pb_height, 49)); pb_offset += r_49
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*25, r_48  -pb_dist, pb_height, 48)); pb_offset += r_48
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*25, r_47  -pb_dist, pb_height, 47)); pb_offset += r_47
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*25, r_46,         pb_height, 46))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*26, 0, 0, "Juz 27"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*26, r_57-pb_dist, pb_height, 57)); pb_offset += r_57
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*26, r_56-pb_dist, pb_height, 56)); pb_offset += r_56
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*26, r_55-pb_dist, pb_height, 55)); pb_offset += r_55
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*26, r_54-pb_dist, pb_height, 54)); pb_offset += r_54
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*26, r_53-pb_dist, pb_height, 53)); pb_offset += r_53
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*26, r_52-pb_dist, pb_height, 52)); pb_offset += r_52
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*26, r_51_2,     pb_height, 51))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*27, 0, 0, "Juz 28"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*27, r_66-pb_dist, pb_height, 66)); pb_offset += r_66
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*27, r_65-pb_dist, pb_height, 65)); pb_offset += r_65
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*27, r_64-pb_dist, pb_height, 64)); pb_offset += r_64
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*27, r_63-pb_dist, pb_height, 63)); pb_offset += r_63
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*27, r_62-pb_dist, pb_height, 62)); pb_offset += r_62
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*27, r_61-pb_dist, pb_height, 61)); pb_offset += r_61
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*27, r_60-pb_dist, pb_height, 60)); pb_offset += r_60
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*27, r_59-pb_dist, pb_height, 59)); pb_offset += r_59
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*27, r_58,       pb_height, 58))

        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*28, 0, 0, "Juz 29"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*28, r_77-pb_dist, pb_height, 77)); pb_offset += r_77
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*28, r_76-pb_dist, pb_height, 76)); pb_offset += r_76
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*28, r_75-pb_dist, pb_height, 75)); pb_offset += r_75
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*28, r_74-pb_dist, pb_height, 74)); pb_offset += r_74
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*28, r_73-pb_dist, pb_height, 73)); pb_offset += r_73
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*28, r_72-pb_dist, pb_height, 72)); pb_offset += r_72
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*28, r_71-pb_dist, pb_height, 71)); pb_offset += r_71
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*28, r_70-pb_dist, pb_height, 70)); pb_offset += r_70
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*28, r_69-pb_dist, pb_height, 69)); pb_offset += r_69
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*28, r_68-pb_dist, pb_height, 68)); pb_offset += r_68
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*28, r_67,       pb_height, 67))


        self.list_rect_progress_bar.append(Rectangle(0, pb_height + pb_line_y0 + pb_lines_dist*29, 0, 0, "Juz 30"))
        pb_offset = pb_line_x0
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_114-pb_dist, pb_height, 114)); pb_offset += r_114
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_113-pb_dist, pb_height, 113)); pb_offset += r_113
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_112-pb_dist, pb_height, 112)); pb_offset += r_112
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_111-pb_dist, pb_height, 111)); pb_offset += r_111
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_110-pb_dist, pb_height, 110)); pb_offset += r_110
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_109-pb_dist, pb_height, 109)); pb_offset += r_109
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_108-pb_dist, pb_height, 108)); pb_offset += r_108
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_107-pb_dist, pb_height, 107)); pb_offset += r_107
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_106-pb_dist, pb_height, 106)); pb_offset += r_106
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_105-pb_dist, pb_height, 105)); pb_offset += r_106
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_104-pb_dist, pb_height, 104)); pb_offset += r_104
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_103-pb_dist, pb_height, 103)); pb_offset += r_103
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_102-pb_dist, pb_height, 102)); pb_offset += r_102
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_101-pb_dist, pb_height, 101)); pb_offset += r_101
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_100-pb_dist, pb_height, 100)); pb_offset += r_100
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_99 -pb_dist,  pb_height, 99)); pb_offset += r_99
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_98 -pb_dist,  pb_height, 98)); pb_offset += r_98
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_97 -pb_dist,  pb_height, 97)); pb_offset += r_97
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_96 -pb_dist,  pb_height, 96)); pb_offset += r_96
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_95 -pb_dist,  pb_height, 95)); pb_offset += r_95
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_94 -pb_dist,  pb_height, 94)); pb_offset += r_94
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_93 -pb_dist,  pb_height, 93)); pb_offset += r_93
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_92 -pb_dist,  pb_height, 92)); pb_offset += r_92
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_91 -pb_dist,  pb_height, 91)); pb_offset += r_91
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_90 -pb_dist,  pb_height, 90)); pb_offset += r_90
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_89 -pb_dist,  pb_height, 89)); pb_offset += r_89
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_88 -pb_dist,  pb_height, 88)); pb_offset += r_88
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_87 -pb_dist,  pb_height, 87)); pb_offset += r_87
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_86 -pb_dist,  pb_height, 86)); pb_offset += r_86
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_85 -pb_dist,  pb_height, 85)); pb_offset += r_85
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_84 -pb_dist,  pb_height, 84)); pb_offset += r_84
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_83 -pb_dist,  pb_height, 83)); pb_offset += r_83
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_82 -pb_dist,  pb_height, 82)); pb_offset += r_82
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_81 -pb_dist,  pb_height, 81)); pb_offset += r_81
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_80 -pb_dist,  pb_height, 80)); pb_offset += r_80
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_79 -pb_dist,  pb_height, 79)); pb_offset += r_79
        self.list_rect_progress_bar.append(Rectangle(pb_offset, pb_line_y0 + pb_lines_dist*29, r_78,         pb_height, 78))


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

        # Create Matrix Rectangles
        self.list_rect_matrix = []
        for i in range(self.rects_per_col):
            for j in range(self.rects_per_line):
                x = 155+ (self.rects_per_line-1-j) * 35 # from left to right
                y = 15 + i * 20
                chapter_num = i * (self.rects_per_line) + j + 1
                self.list_rect_matrix.append(Rectangle(x, y, 30, 10, chapter_num))

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
                        rect.y <= event.y <= rect.y + rect.height and
                        isinstance(rect.caption, int)):
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
        for rect in self.list_rect_matrix:
            rect.color = rect.on_color if rect.caption in self.user.mem_chapters else rect.off_color

        # Refresh Progress Bar Rectangles
        for rect in self.list_rect_progress_bar:
            rect.color = rect.on_color if rect.caption in self.user.mem_chapters else rect.off_color
        
        self.queue_draw() # ensure Redraw


    def refresh_stats_label(self):
        self.label_stats.set_markup(
            f"<big><b>Chapters:</b> {self.user.n_mem_chapters} ({round(self.user.n_mem_chapters / self.book.n_chapters * 100, 1)}%)</big>\n"
            f"<big><b>Verses:</b> {self.user.n_mem_verses} ({round(self.user.n_mem_verses / self.book.n_verses * 100, 1)}%)</big>\n"
            f"<big><b>Words:</b> {self.user.n_mem_words} ({round(self.user.n_mem_words / self.book.n_words * 100, 1)}%)</big>\n"
            f"<big><b>Letters:</b> {self.user.n_mem_letters} ({round(self.user.n_mem_letters / self.book.n_letters * 100, 1)}%)</big>"
        )
