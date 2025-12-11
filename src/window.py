import os
import csv
import cairo
import gi

from gi.repository import Gtk, Gio, Gdk, GdkPixbuf, Pango

from .chapter_rectangle import ChapterRectangle
from .color_utils import ColorUtils
from .download_manager import DownloadManager

class Window(Gtk.Window):
    def __init__(self,
        app,
        bars_sizes_path,
        app_icon_path = None
    ):
        super().__init__()

        self.app = app

        self.color_utils = ColorUtils()
        self.download_manager = DownloadManager(self)


        self._set_icon_from_file(app_icon_path)

        # Rectangles color
        self.default_rect_color_hex = "#00CC00FF"
        rect_color_hex = self.app.preferences_manager.read_rect_color_from_file()
        if not rect_color_hex or not self.color_utils.valid_color_hex(rect_color_hex):
            rect_color_hex = self.default_rect_color_hex
            self.app.preferences_manager.write_rect_color_to_file(rect_color_hex)
        self.rect_color = self.color_utils.hex_to_rgba(rect_color_hex)


        # Shortcuts
        accel_group = Gtk.AccelGroup()
        self.add_accel_group(accel_group)

        self.list_shortcuts = []

        self._add_shortcut(accel_group, "Quit",               "<control>Q", self._on_ctrl_q)
        self._add_shortcut(accel_group, "Save Progress Bars", "<control>S", self._on_ctrl_s)


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

        # Keyboard Shortcurts Button
        bt = Gtk.ModelButton(label="Keyboard Shortcuts")
        bt.connect("clicked", self._on_click_shortcuts)
        vbox.pack_start(bt, False, True, 10)

        # About Button
        bt = Gtk.ModelButton(label=f"About {self.app.name}")
        bt.connect("clicked", self._on_click_about)
        vbox.pack_start(bt, False, True, 10)

        vbox.show_all()
        popover_menu.add(vbox)
        popover_menu.set_position(Gtk.PositionType.BOTTOM)


        # Header Bar
        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        headerbar.props.title = self.app.name
        self.set_titlebar(headerbar)


        # Menu Button
        bt = Gtk.MenuButton(popover=popover_menu)
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        img_icon = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        bt.add(img_icon)
        bt.set_tooltip_text("Main Menu")
        headerbar.pack_end(bt)

        # Save Button
        bt = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-save-symbolic")
        img_icon = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        bt.add(img_icon)
        bt.set_tooltip_text("Save Progress Bars")
        bt.connect("clicked", self._on_click_save)
        headerbar.pack_end(bt)

        # Color Chooser Button
        bt = Gtk.Button()
        icon = Gio.ThemedIcon(name="preferences-color-symbolic")
        img_icon = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        bt.add(img_icon)
        bt.set_tooltip_text("Select Color")
        bt.connect("clicked", self._on_click_color_chooser)
        headerbar.pack_start(bt)


        # Stack
        stack = Gtk.Stack()


        # Create Chapter Rectangles of progress bars
        self.pb_x0 = 20  # initial x
        self.pb_y0 = 20  # initial y
        self.pb_height = 10  # bar height
        self.pb_lines_dist = self.pb_height + 2  # distance between lines
        self.pb_dist = 1  # distance between 2 bars


        # Create Chapter Rectangles
        self.list_rects_pb = self._create_pb_rects_from_file(bars_sizes_path)
        self.list_rects_matrix = self._create_matrix_rects(6, 19)

        self._refresh_rects_colors()

        # Progress Bars Tab
        drawingarea_pb = Gtk.DrawingArea()
        drawingarea_pb.connect("draw", self._draw_juz_text)
        drawingarea_pb.connect("draw", self._draw_progress_bars)
        drawingarea_pb.connect("button-press-event", self._on_click_progress_bar)
        drawingarea_pb.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        stack.add_titled(drawingarea_pb, "bars", "Progress Bars")

        # Matrix Tab
        drawingarea_matrix = Gtk.DrawingArea()
        drawingarea_matrix.connect("draw", self._draw_matrix)
        drawingarea_matrix.connect("button-press-event", self._on_click_matrix)
        drawingarea_matrix.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        stack.add_titled(drawingarea_matrix, "matrix", "Matrix")


        # List Tab
        checkbutton_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        for chapter in self.app.book.list_chapters:
            checkbutton = Gtk.CheckButton(label=f"{chapter.number}. ({chapter.name_latin}) {chapter.name_arabic}")
            checkbutton.modify_font(Pango.FontDescription("11"))
            if chapter.number in self.app.user.list_mem_chapters:
                checkbutton.set_active(True)
            checkbutton.connect("toggled", lambda bt, obj=chapter: self._on_toggle_checkbox(bt, obj))
            checkbutton_container.pack_start(checkbutton, False, False, 0)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(checkbutton_container)
        stack.add_titled(scrolled_window, "list", "List")


        # Stats Tab
        self.label_stats = Gtk.Label()
        self._refresh_stats_label()
        stack.add_titled(self.label_stats, "stats", "Stats")


        # Chapter Popover when clicking on a chapter rectangle
        self.popover_chapter = Gtk.Popover()
        self.label_chapter = Gtk.Label()
        self.popover_chapter.add(self.label_chapter)

        # State attributes for managing popover clicks
        self.is_popover_chapter_active = False
        self.cursor_x_at_popover = None
        self.cursor_y_at_popover = None

        # Connect a click event to the whole window to detect clicks outside the popover
        self.connect("button-press-event", self._on_click_outside_popover)


        # Stack Switcher
        stackswitcher = Gtk.StackSwitcher()
        stackswitcher.set_stack(stack)
        stackswitcher.set_halign(Gtk.Align.CENTER)

        outerbox.pack_start(stackswitcher, False, False, 0)
        outerbox.pack_start(stack, True, True, 0)


    def _set_icon_from_file(self, icon_path):
        if icon_path:
            try:
                self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_path, 64, 64, True)
                self.set_icon(self.pixbuf)
            except:
                self.pixbuf = None
                print(f'Failed to load icon from "{self.app_icon_path}"')

    def _add_shortcut(self, accel_group, action, accelerator, callback):
        key, mod = Gtk.accelerator_parse(accelerator)
        accel_group.connect(key, mod, Gtk.AccelFlags.VISIBLE, callback)

        self.list_shortcuts.append((action, key, mod))


    def _on_ctrl_q(self, accel_group, window, key, modifier):
        self.app.quit()

    def _on_ctrl_s(self, accel_group, window, key, modifier):
        self.download_manager.open_save_dialog()


    def _on_click_outside_popover(self, widget, event):
        # Hide only when clicking in a point that is not the one that opened the popover
        if (self.is_popover_chapter_active == True and
            event.x != self.cursor_x_at_popover and
            event.y != self.cursor_y_at_popover
        ):
            self.is_popover_chapter_active = False
            self.popover_chapter.hide()

    def _on_click_progress_bar(self, widget, event):
        if (event.type == Gdk.EventType.BUTTON_PRESS and
            event.button == Gdk.BUTTON_PRIMARY
        ):
            for rect in self.list_rects_pb:
                if (rect.x <= event.x <= rect.x + rect.width and
                    rect.y <= event.y <= rect.y + rect.height and
                    isinstance(rect.caption, int)
                ):
                    self._show_chapter_popover(rect, widget, event)
                    break

    def _on_click_matrix(self, widget, event):
        if (event.type == Gdk.EventType.BUTTON_PRESS and
            event.button == Gdk.BUTTON_PRIMARY
        ):
            e_x, e_y = event.x, event.y
            for rect in self.list_rects_matrix:
                r_x = rect.x
                r_y = rect.y
                r_w = rect.width
                r_h = rect.height
                if (r_x <= e_x <= r_x + r_w and
                    r_y <= e_y <= r_y + r_h
                ):
                    self._show_chapter_popover(rect, widget, event)
                    break


    def _on_toggle_checkbox(self, button, chapter):
        if button.get_active():
            self.app.user.add_mem_chapter(chapter)
        else:
            self.app.user.rm_mem_chapter(chapter)

        self.app.user_data_changed = True

        self._refresh_stats_label()
        self._refresh_rects_colors()

    def _on_click_color_chooser(self, widget):
        color_chooser = Gtk.ColorChooserDialog("Select rectangle color", self)

        color_chooser.set_rgba(self.color_utils.hex_to_rgba(self.default_rect_color_hex))  # default color

        response = color_chooser.run()
        if response == Gtk.ResponseType.OK:
            color = color_chooser.get_rgba()
            self._paint_rects(color)
            self.app.preferences_manager.write_rect_color_to_file(self.color_utils.rgba_to_hex(color))

        color_chooser.destroy()

    def _on_click_save(self, widget):
        self.download_manager.open_save_dialog()

    def _on_click_shortcuts(self, button):
        dialog = Gtk.Dialog("Shortcuts", self, Gtk.DialogFlags.MODAL)

        dialog.set_default_size(300, 70)
        dialog.set_resizable(False)

        content_area = dialog.get_content_area()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        for action, key, mod in self.list_shortcuts:
            accel_label = Gtk.AccelLabel(label=action)
            accel_label.set_accel(key, mod)

            vbox.pack_start(accel_label, False, True, 0)

        content_area.add(vbox)
        dialog.show_all()

        dialog.run()
        dialog.destroy()

    def _on_click_about(self, widget):
        about = Gtk.AboutDialog(transient_for=self, modal=True)
        about.set_program_name(self.app.name)
        about.set_version(self.app.version)
        about.set_comments(self.app.description)
        about.set_website(self.app.website_url)
        about.set_website_label(self.app.website_label)
        about.set_authors(self.app.authors)
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_copyright(self.app.copyright)

        if self.pixbuf:
            about.set_logo(self.pixbuf)

        about.connect("response", lambda dialog, response: dialog.destroy())
        about.present()


    def _create_pb_rects_from_file(self, bars_sizes_path):
        list_rects_pb = []
        prev_juz = None

        if not os.path.isfile(bars_sizes_path):
            raise FileNotFoundError(f'Failed to find bars sizes file "{self.bars_sizes_path}"')
        try:
            with open(bars_sizes_path, mode="r") as f:
                reader = csv.reader(f)
                for line in reader:
                    juz         = int(line[0])
                    chapter_num = int(line[1])
                    length      = float(line[3])

                    if juz != prev_juz:
                        num_pos = 0 if juz >= 10 else self.pb_x0/4
                        pb_offset = self.pb_x0

                    list_rects_pb.append(
                        ChapterRectangle(
                            pb_offset,
                            self.pb_y0 + self.pb_lines_dist*(juz-1),
                            length-self.pb_dist,
                            self.pb_height,
                            chapter_num,
                            self.rect_color
                        )
                    )

                    pb_offset += length
                    prev_juz = juz

            return list_rects_pb
        except Exception as e:
            print(f'Failed to load bars sizes files at "{self.preferences_path}": {e}')

    def _create_matrix_rects(self, rects_per_line, rects_per_col):
        list_rects_matrix = []
        for i in range(rects_per_col):
            for j in range(rects_per_line):
                x = 155 + (rects_per_line-1-j)*35  # from left to right
                y = 15 + i*20
                chapter_num = i*(rects_per_line) + j + 1
                list_rects_matrix.append(ChapterRectangle(x, y, 30, 10, chapter_num, self.rect_color))
        return list_rects_matrix

    def create_img(self):
        max_x = max(rect.x + rect.width  for rect in self.list_rects_pb)
        max_y = max(rect.y + rect.height for rect in self.list_rects_pb)

        # Add padding
        surface_width  = int(max_x + self.pb_x0)
        surface_height = int(max_y + self.pb_y0)

        # Create a Cairo surface
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, surface_width, surface_height)
        cr = cairo.Context(surface)

        # Set background
        cr.set_source_rgb(1, 1, 1)
        cr.paint()

        self._draw_progress_bars(widget=None, cr=cr)
        self._draw_juz_text(widget=None, cr=cr)

        return surface


    def _draw_matrix(self, widget, cr):
        for rect in self.list_rects_matrix:
            cr.set_source_rgba(rect.color.red, rect.color.green, rect.color.blue, rect.color.alpha)
            cr.rectangle(rect.x, rect.y, rect.width, rect.height)
            cr.fill()

    def _draw_juz_text(self, widget, cr: cairo.Context):
        cr.set_source_rgb(0.7, 0.7, 0.7)
        cr.set_font_size(10)

        cr.move_to(0, self.pb_y0 - 5)
        cr.show_text("Juz'")

        for juz in range(1, 30+1):
            # Calculate position - offset for single-digit task numbers
            num_pos = 0 if juz >= 10 else self.pb_x0 / 4
            x_pos = num_pos
            y_pos = self.pb_y0 + self.pb_lines_dist * (juz-1) + self.pb_height - 2

            # Draw the Juz' line label
            cr.move_to(x_pos, y_pos)
            cr.show_text(str(juz))

    def _draw_progress_bars(self, widget, cr: cairo.Context):
        for rect in self.list_rects_pb:
            cr.set_source_rgba(rect.color.red, rect.color.green, rect.color.blue, rect.color.alpha)
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


    def _paint_rects(self, color: Gdk.RGBA):
        r = color.red
        g = color.green
        b = color.blue
        a = color.alpha

        for rect in self.list_rects_matrix:
            rect.color_on = Gdk.RGBA(r,g,b,a)
        for rect in self.list_rects_pb:
            rect.color_on = Gdk.RGBA(r,g,b,a)

        self._refresh_rects_colors()

    def _refresh_rects_colors(self):
        for rect in self.list_rects_matrix:
            rect.paint_on() if rect.caption in self.app.user.list_mem_chapters else rect.paint_off()
        for rect in self.list_rects_pb:
            rect.paint_on() if rect.caption in self.app.user.list_mem_chapters else rect.paint_off()

    def _refresh_stats_label(self):
        self.label_stats.set_markup(
            f"<span font='13'><b>Chapters:</b> {self.app.user.n_mem_chapters} ({round(self.app.user.n_mem_chapters / self.app.book.n_chapters * 100, 1)}%)</span>\n"
            f"<span font='13'><b>Verses:</b> {self.app.user.n_mem_verses} ({round(self.app.user.n_mem_verses / self.app.book.n_verses * 100, 1)}%)</span>\n"
            f"<span font='13'><b>Words:</b> {self.app.user.n_mem_words} ({round(self.app.user.n_mem_words / self.app.book.n_words * 100, 1)}%)</span>\n"
            f"<span font='13'><b>Letters:</b> {self.app.user.n_mem_letters} ({round(self.app.user.n_mem_letters / self.app.book.n_letters * 100, 1)}%)</span>"
        )
