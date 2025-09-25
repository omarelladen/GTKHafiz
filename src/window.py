import os
import csv

import cairo
import gi
from gi.repository import Gtk, Gio, Gdk, GdkPixbuf

from rectangle import Rectangle

class Window(Gtk.Window):
    def __init__(self, 
        app,
        bar_sizes_file,
        icon_path = None,
    ):
        super().__init__()
        
        self.app = app

        # Icon
        if icon_path:
            try:
                self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_path, 64, 64, True)
                self.set_icon(self.pixbuf)
            except:
                self.pixbuf = None
                print(f'Failed to load icon from "{icon_path}"')

        # Window dimensions
        self.set_size_request(580, 550)
        self.set_resizable(False)
        self.set_border_width(6)

        # Vertical Box
        outerbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(outerbox)

        # Menu Popover
        popover_menu = Gtk.Popover()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        bt_about = Gtk.ModelButton(label="About GTKHafiz")
        bt_about.connect("clicked", self._on_click_about)
        vbox.pack_start(bt_about, False, True, 10)
        vbox.show_all()
        popover_menu.add(vbox)
        popover_menu.set_position(Gtk.PositionType.BOTTOM)

        # Header Bar
        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        headerbar.props.title = "GTKHafiz"
        self.set_titlebar(headerbar)

        # Menu Button
        bt_menu = Gtk.MenuButton(popover=popover_menu)
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        img_icon = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        bt_menu.add(img_icon)
        headerbar.pack_end(bt_menu)

        # Stack
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        # Create Progress Bars Rectangles
        self.pb_line_x0 = 20  # initial x
        self.pb_line_y0 = 20  # initial y
        self.pb_height = 10  # bar height
        self.pb_lines_dist = self.pb_height + 2  # distance between lines
        self.pb_dist = 1  # distance between 2 bars
        
        self.list_rect_progress_bar = []

        prev_juz = None
        with open(bar_sizes_file, mode='r') as file:
            reader = csv.reader(file)
            for line in reader:
                juz = int(line[0])
                chapter = int(line[1])
                length = float(line[3])
                if juz != prev_juz:
                    num_pos = 0 if juz >= 10 else self.pb_line_x0/4
                    self.pb_offset = self.pb_line_x0
                self.list_rect_progress_bar.append(Rectangle(self.pb_offset,
                                                             self.pb_line_y0 + self.pb_lines_dist*(juz-1), 
                                                             length-self.pb_dist,
                                                             self.pb_height,
                                                             chapter))
                self.pb_offset += length
                prev_juz = juz

        # Progress Bars Tab
        drawingarea_progress_bar = Gtk.DrawingArea()
        drawingarea_progress_bar.connect("draw", self._on_draw_text)
        drawingarea_progress_bar.connect("draw", self._on_draw_progress_bar)
        drawingarea_progress_bar.connect("button-press-event", self._on_click_progress_bar)
        drawingarea_progress_bar.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        stack.add_titled(drawingarea_progress_bar, "bars", "Bars")

        # Matrix Tab
        rects_per_col = 19
        rects_per_line = 6
        drawingarea_matrix = Gtk.DrawingArea()
        drawingarea_matrix.connect("draw", self._on_draw_matrix)
        drawingarea_matrix.connect("button-press-event", self._on_click_matrix)
        drawingarea_matrix.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        stack.add_titled(drawingarea_matrix, "matrix", "Matrix")

        # Create Matrix Rectangles
        self.list_rect_matrix = []
        for i in range(rects_per_col):
            for j in range(rects_per_line):
                x = 155 + (rects_per_line-1-j)*35  # from left to right
                y = 15 + i*20
                chapter_num = i*(rects_per_line) + j + 1
                self.list_rect_matrix.append(Rectangle(x, y, 30, 10, chapter_num))

        # Create Rectangles for Progress Bar and Matrix
        self._refresh_rectangles()

        # List Tab
        checkbutton_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        for chapter in self.app.book.list_chapters:
            checkbutton = Gtk.CheckButton(label=f"{chapter.number}. ({chapter.name_latin}) {chapter.name_arabic}")
            if chapter.number in self.app.user.list_mem_chapters:
                checkbutton.set_active(True)
            checkbutton.connect("toggled", lambda btn, obj=chapter: self._on_toggle_checkbox(btn, obj))
            checkbutton_container.pack_start(checkbutton, False, False, 0)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(checkbutton_container)
        stack.add_titled(scrolled_window, "list", "List")

        # Stats Tab
        self.label_stats = Gtk.Label()
        self._refresh_stats_label()
        stack.add_titled(self.label_stats, "stats", "Statistics")

        # Chapter Popover
        self.popover_chapter = Gtk.Popover()
        self.label_chapter = Gtk.Label()
        self.popover_chapter.add(self.label_chapter)

        self.is_popover_chapter_active = False
        self.cursor_x_at_popover = None
        self.cursor_y_at_popover = None

        # All clicks will be checked to be able to hide the chapter popovers
        self.connect("button-press-event", self._on_click_outside_popover)

        # Stack Switcher
        stackswitcher = Gtk.StackSwitcher()
        stackswitcher.set_stack(stack)
        stackswitcher.set_halign(Gtk.Align.CENTER)  # horizontal

        outerbox.pack_start(stackswitcher, False, True, 0)
        outerbox.pack_start(stack, True, True, 0)

    def _on_click_outside_popover(self, widget, event):
        if (self.is_popover_chapter_active == True and
            event.x != self.cursor_x_at_popover and
            event.y != self.cursor_y_at_popover):
            self.is_popover_chapter_active = False
            self.popover_chapter.hide()

    def _on_click_progress_bar(self, widget, event):
        if (event.type == Gdk.EventType.BUTTON_PRESS and
            event.button == Gdk.BUTTON_PRIMARY):
            for rect in self.list_rect_progress_bar:
                if (rect.x <= event.x <= rect.x + rect.width and
                    rect.y <= event.y <= rect.y + rect.height and
                    isinstance(rect.caption, int)):
                    self._show_chapter_popover(rect, widget, event)
                    break

    def _on_click_matrix(self, widget, event):
        if (event.type == Gdk.EventType.BUTTON_PRESS and
            event.button == Gdk.BUTTON_PRIMARY):
            e_x, e_y = event.x, event.y
            for rect in self.list_rect_matrix:
                r_x = rect.x
                r_y = rect.y
                r_w = rect.width
                r_h = rect.height
                if (r_x <= e_x <= r_x + r_w and
                    r_y <= e_y <= r_y + r_h):
                    self._show_chapter_popover(rect, widget, event)
                    break

    def _on_click_about(self, widget):
        about = Gtk.AboutDialog(transient_for=self, modal=True)

        about.set_program_name("GTKHafiz")
        about.set_version("0.3.0")
        about.set_comments("Track Qur'an memorization visually")
        about.set_website("https://github.com/omarelladen/GTK-Hafiz")
        about.set_website_label("Repository")
        about.set_authors(["Omar El Laden"])
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_copyright("Copyright © 2025 Omar El Laden")

        if self.pixbuf:
            about.set_logo(self.pixbuf)

        about.connect("response", lambda dialog, response: dialog.destroy())
        about.present()

    def _on_toggle_checkbox(self, button, chapter):
        # Checkbox activation
        if button.get_active():
            self.app.user.list_mem_chapters.append(chapter.number)
            self.app.user.n_mem_chapters += 1
            self.app.user.n_mem_verses   += chapter.n_verses
            self.app.user.n_mem_words    += chapter.n_words
            self.app.user.n_mem_letters  += chapter.n_letters

        # Checkbox deactivation
        else:
            self.app.user.list_mem_chapters.remove(chapter.number)
            self.app.user.n_mem_chapters -= 1
            self.app.user.n_mem_verses   -= chapter.n_verses
            self.app.user.n_mem_words    -= chapter.n_words
            self.app.user.n_mem_letters  -= chapter.n_letters

        self.app.user_data_changed = True

        # Refresh
        self._refresh_stats_label()
        self._refresh_rectangles()

    def _on_draw_matrix(self, widget, cr):
        for rect in self.list_rect_matrix:
            r_x = rect.x
            r_y = rect.y
            r_w = rect.width
            r_h = rect.height
            r_color = rect.color
            cr.set_source_rgb(r_color[0], r_color[1], r_color[2])
            cr.rectangle(r_x, r_y, r_w, r_h)
            cr.fill()

    def _on_draw_text(self, widget, cr: cairo.Context):
        cr.set_source_rgb(1, 1, 1)
        cr.set_font_size(10)

        for juz in range(1, 30+1):
            # Calculate position - offset for single-digit task numbers
            num_pos = 0 if juz >= 10 else self.pb_line_x0 / 4
            x_pos = num_pos
            y_pos = self.pb_line_y0 + self.pb_lines_dist * (juz - 1) + self.pb_height - 2

            # Draw the Juz' line label
            cr.move_to(x_pos, y_pos)
            cr.show_text(str(juz))

    def _on_draw_progress_bar(self, widget, cr: cairo.Context):
        for rect in self.list_rect_progress_bar:
            cr.set_source_rgb(*rect.color)
            cr.rectangle(rect.x, rect.y, rect.width, rect.height)

            # Juz' indication
            if isinstance(rect.caption, str) and "Juz'" in rect.caption:
                cr.show_text(rect.caption.replace("Juz' ", ""))

            cr.fill()

    def _show_chapter_popover(self, rect, widget, event):
        self.label_chapter.set_text(f"{rect.caption}")

        e_x = event.x
        e_y = event.y

        # Set popover position
        self.popover_chapter.set_relative_to(widget)
        self.popover_chapter.set_pointing_to(rect)
        self.popover_chapter.set_position(Gtk.PositionType.TOP)
        self.popover_chapter.show_all()

        # Set current popover location and state so that it is gets hiden only by clicking outside this point
        self.cursor_x_at_popover = e_x
        self.cursor_y_at_popover = e_y
        self.is_popover_chapter_active = True

    def _refresh_rectangles(self):
        # Refresh Matrix Rectangles
        for rect in self.list_rect_matrix:
            rect.color = rect.color_on if rect.caption in self.app.user.list_mem_chapters else rect.color_off
    
        # Refresh Progress Bar Rectangles
        for rect in self.list_rect_progress_bar:
            rect.color = rect.color_on if rect.caption in self.app.user.list_mem_chapters else rect.color_off

    def _refresh_stats_label(self):
        self.label_stats.set_markup(
            f"<big><b>Chapters:</b> {self.app.user.n_mem_chapters} ({round(self.app.user.n_mem_chapters / self.app.book.n_chapters * 100, 1)}%)</big>\n"
            f"<big><b>Verses:</b> {self.app.user.n_mem_verses} ({round(self.app.user.n_mem_verses / self.app.book.n_verses * 100, 1)}%)</big>\n"
            f"<big><b>Words:</b> {self.app.user.n_mem_words} ({round(self.app.user.n_mem_words / self.app.book.n_words * 100, 1)}%)</big>\n"
            f"<big><b>Letters:</b> {self.app.user.n_mem_letters} ({round(self.app.user.n_mem_letters / self.app.book.n_letters * 100, 1)}%)</big>"
        )
