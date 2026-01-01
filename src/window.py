import os
import csv
import cairo

from gi.repository import Gtk, Gio, Gdk, GdkPixbuf, Pango

from .chapter_rectangle import ChapterRectangle
from .color_utils import ColorUtils
from .download_manager import DownloadManager
from .import_manager import ImportManager


class Window(Gtk.Window):
    def __init__(
        self,
        app,
        user,
        book,
        preferences_manager,
        bars_sizes_path,
        app_icon_path=None
    ):
        super().__init__()

        self.app = app
        self.user = user
        self.book = book
        self.preferences_manager = preferences_manager

        self.color_utils = ColorUtils()
        self.download_manager = DownloadManager(self)
        self.import_manager = ImportManager(self)

        # Icon
        self._set_icon_from_file(app_icon_path)


        # Rectangles color
        self.default_rect_color_hex = "#00CC00FF"
        rect_color_hex = self.preferences_manager.read_rect_color_from_file()
        if (not rect_color_hex or
            not self.color_utils.is_valid_color_hex(rect_color_hex)
        ):
            rect_color_hex = self.default_rect_color_hex
            self.preferences_manager.write_rect_color_to_file(rect_color_hex)
        self.rect_color = self.color_utils.hex_to_rgba(rect_color_hex)


        # Shortcuts
        accelgroup = Gtk.AccelGroup()
        self.add_accel_group(accelgroup)

        self.list_shortcuts = []

        self._add_shortcut(accelgroup, "Quit",         "<ctrl>Q", self._on_ctrl_q)
        self._add_shortcut(accelgroup, "Export Image", "<ctrl>S", self._on_ctrl_s)


        # Window dimensions
        self.set_size_request(580, 550)
        self.set_resizable(False)
        self.set_border_width(6)


        # Main Vertical Box
        box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_main)

        # Stack - holds multiple pages and shows one at a time
        stack = Gtk.Stack()

        # Stack Switcher - creates the page buttons to switch the stack
        stackswitcher = Gtk.StackSwitcher()
        stackswitcher.set_stack(stack)
        stackswitcher.set_halign(Gtk.Align.CENTER)

        box_main.pack_start(stackswitcher, False, False, 0)
        box_main.pack_start(stack, True, True, 0)


        # Menu Popover
        popover_menu = Gtk.Popover()
        box_menu = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        padding_menu = 2

        # Import Button
        bt = Gtk.ModelButton(label="Import Chapters")
        bt.connect("clicked", self._on_click_import)
        box_menu.pack_start(bt, False, True, padding_menu)

        # Save Button
        bt = Gtk.ModelButton(label="Export Image")
        bt.connect("clicked", self._on_click_save)
        box_menu.pack_start(bt, False, True, padding_menu)

        # Keyboard Shortcurts Button
        bt = Gtk.ModelButton(label="Keyboard Shortcuts")
        bt.connect("clicked", self._on_click_shortcuts)
        box_menu.pack_start(bt, False, True, padding_menu)

        # About Button
        bt = Gtk.ModelButton(label=f"About {self.app.name}")
        bt.connect("clicked", self._on_click_about)
        box_menu.pack_start(bt, False, True, padding_menu)

        box_menu.show_all()
        popover_menu.add(box_menu)
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

        # Color Chooser Button
        bt = Gtk.Button()
        icon = Gio.ThemedIcon(name="preferences-color-symbolic")
        img_icon = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        bt.add(img_icon)
        bt.set_tooltip_text("Select Color")
        bt.connect("clicked", self._on_click_color_chooser)
        headerbar.pack_start(bt)


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


        # Progress Bars Page
        drawingarea_pb = Gtk.DrawingArea()
        drawingarea_pb.connect("draw", self._draw_juz_text)
        drawingarea_pb.connect("draw", self._draw_progress_bars)
        drawingarea_pb.connect("button-press-event", self._on_click_progress_bar)
        drawingarea_pb.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        stack.add_titled(drawingarea_pb, "bars", "Progress Bars")

        # Matrix Page
        drawingarea_matrix = Gtk.DrawingArea()
        drawingarea_matrix.connect("draw", self._draw_matrix)
        drawingarea_matrix.connect("button-press-event", self._on_click_matrix)
        drawingarea_matrix.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        stack.add_titled(drawingarea_matrix, "matrix", "Matrix")

        # List Page
        box_checkbutton = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.checkbuttons = {}
        for chapter in self.book.list_chapters:
            checkbutton = Gtk.CheckButton(
                label=f"{chapter.number}. "
                      f"({chapter.name_latin}) "
                      f"{chapter.name_arabic}"
            )
            checkbutton.modify_font(Pango.FontDescription("11"))

            self.checkbuttons[chapter.number] = checkbutton

            if chapter.number in self.user.list_mem_chapters:
                checkbutton.set_active(True)
            checkbutton.connect(
                "toggled",
                lambda bt, obj=chapter: self._on_toggle_checkbox(bt, obj)
            )
            box_checkbutton.pack_start(checkbutton, False, False, 0)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC
        )
        scrolledwindow.add(box_checkbutton)
        stack.add_titled(scrolledwindow, "list", "List")


        # Stats Page
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

        # Connect a click event to the whole window
        # to detect clicks outside the popover
        self.connect("button-press-event", self._on_click_outside_popover)


    def _refresh_visual_data(self):
        self._refresh_stats_label()
        self._refresh_rects_colors()

        self.app.user_data_changed = True

    def _set_icon_from_file(self, icon_path):
        if icon_path:
            try:
                self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    icon_path, 64, 64, True
                )
                self.set_icon(self.pixbuf)
            except:
                self.pixbuf = None
                print(f'Failed to load icon from "{icon_path}"')

    def _add_shortcut(self, accelgroup, action, accelerator, callback):
        key, mod = Gtk.accelerator_parse(accelerator)
        accelgroup.connect(key, mod, Gtk.AccelFlags.VISIBLE, callback)

        self.list_shortcuts.append((action, key, mod))

    def _open_save_dialog(self):
        self.download_manager.open_save_dialog()

    def _on_ctrl_q(self, accelgroup, window, key, modifier):
        self.app.quit()

    def _on_ctrl_s(self, accelgroup, window, key, modifier):
        self._open_save_dialog()


    def _on_click_outside_popover(self, widget, event):
        # Hide only when clicking in a point
        # that is not the one that opened the popover
        if (self.is_popover_chapter_active and
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
            self.user.add_mem_chapter(chapter)
        else:
            self.user.rm_mem_chapter(chapter)

        self._refresh_visual_data()


    def _on_click_color_chooser(self, widget):
        color_chooser_dialog = Gtk.ColorChooserDialog(
            "Select Rectangle Color", self
        )

        # Default color
        color_chooser_dialog.set_rgba(
            self.color_utils.hex_to_rgba(self.default_rect_color_hex)
        )

        response = color_chooser_dialog.run()
        if response == Gtk.ResponseType.OK:
            color = color_chooser_dialog.get_rgba()
            self._paint_rects(color)
            self.preferences_manager.write_rect_color_to_file(
                self.color_utils.rgba_to_hex(color)
            )

        color_chooser_dialog.destroy()

    def _on_click_save(self, widget):
        self._open_save_dialog()

    def _on_click_import(self, widget):
        list_imported_chapters = self.import_manager.run_dialog()

        if list_imported_chapters:

            # Update User data
            for chapter in self.book.list_chapters:
                if chapter.number in list_imported_chapters:
                    self.user.add_mem_chapter(chapter)
                else:
                    self.user.rm_mem_chapter(chapter)

            # Mark Checklist
            for chapter_number, checkbutton in self.checkbuttons.items():
                if chapter_number in list_imported_chapters:
                    checkbutton.set_active(True)
                else:
                    checkbutton.set_active(False)

            self._refresh_visual_data()

    def _on_click_shortcuts(self, widget):
        dialog = Gtk.Dialog("Shortcuts", self, Gtk.DialogFlags.MODAL)

        dialog.set_default_size(300, 70)
        dialog.set_resizable(False)

        content_area = dialog.get_content_area()
        box_shortcuts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        for action, key, mod in self.list_shortcuts:
            accellabel = Gtk.AccelLabel(label=action)
            accellabel.set_accel(key, mod)

            box_shortcuts.pack_start(accellabel, False, True, 0)

        content_area.add(box_shortcuts)
        dialog.show_all()

        dialog.run()
        dialog.destroy()

    def _on_click_about(self, widget):
        about_dialog = Gtk.AboutDialog(transient_for=self, modal=True)
        about_dialog.set_program_name(self.app.name)
        about_dialog.set_version(self.app.version)
        about_dialog.set_comments(self.app.description)
        about_dialog.set_website(self.app.website_url)
        about_dialog.set_website_label(self.app.website_label)
        about_dialog.set_authors(self.app.authors)
        about_dialog.set_license_type(Gtk.License.GPL_3_0)
        about_dialog.set_copyright(self.app.copyright)

        if self.pixbuf:
            about_dialog.set_logo(self.pixbuf)

        about_dialog.connect(
            "response",
            lambda dialog, response: dialog.destroy()
        )
        about_dialog.present()


    def _create_pb_rects_from_file(self, bars_sizes_path):
        list_rects_pb = []
        prev_juz = None

        if not os.path.isfile(bars_sizes_path):
            raise FileNotFoundError(
                f'Failed to find bars sizes file "{bars_sizes_path}"'
            )
        try:
            with open(bars_sizes_path, mode="r") as f:
                reader = csv.reader(f)
                for line in reader:
                    juz         = int(line[0])
                    chapter_num = int(line[1])
                    width       = float(line[3])

                    if juz != prev_juz:
                        pb_offset = self.pb_x0

                    list_rects_pb.append(
                        ChapterRectangle(
                            pb_offset,
                            self.pb_y0 + self.pb_lines_dist*(juz-1),
                            width-self.pb_dist,
                            self.pb_height,
                            chapter_num,
                            self.rect_color
                        )
                    )

                    pb_offset += width
                    prev_juz = juz

            return list_rects_pb
        except Exception as e:
            raise Exception(
                f'Failed to load bars sizes files at "{bars_sizes_path}": {e}'
            )

    def _create_matrix_rects(self, rects_per_line, rects_per_col):
        list_rects_matrix = []
        for i in range(rects_per_col):
            for j in range(rects_per_line):
                x = 155 + (rects_per_line-1-j)*35  # from left to right
                y = 15 + i*20
                chapter_num = i*(rects_per_line) + j + 1
                list_rects_matrix.append(
                    ChapterRectangle(
                        x,
                        y,
                        30,
                        10,
                        chapter_num,
                        self.rect_color
                    )
                )
        return list_rects_matrix


    def _draw_matrix(self, widget, cr):
        for rect in self.list_rects_matrix:
            cr.set_source_rgba(
                rect.color.red,
                rect.color.green,
                rect.color.blue,
                rect.color.alpha
            )
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
            y_pos = (
                self.pb_y0
                + self.pb_lines_dist * (juz-1)
                + self.pb_height - 2
            )

            # Draw the Juz' line label
            cr.move_to(x_pos, y_pos)
            cr.show_text(str(juz))

    def _draw_progress_bars(self, widget, cr: cairo.Context):
        for rect in self.list_rects_pb:
            cr.set_source_rgba(
                rect.color.red,
                rect.color.green,
                rect.color.blue,
                rect.color.alpha
            )
            cr.rectangle(rect.x, rect.y, rect.width, rect.height)

            # Juz' indication
            if isinstance(rect.caption, str) and "Juz'" in rect.caption:
                cr.show_text(rect.caption.replace("Juz' ", ""))

            cr.fill()

    def create_img(self):
        max_x = max(rect.x + rect.width  for rect in self.list_rects_pb)
        max_y = max(rect.y + rect.height for rect in self.list_rects_pb)

        # Add padding
        surface_width  = int(max_x + self.pb_x0)
        surface_height = int(max_y + self.pb_y0)

        # Create a Cairo surface
        surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, surface_width, surface_height
        )
        cr = cairo.Context(surface)

        # Set background
        cr.set_source_rgb(1, 1, 1)
        cr.paint()

        self._draw_progress_bars(widget=None, cr=cr)
        self._draw_juz_text(widget=None, cr=cr)

        return surface


    def _show_chapter_popover(self, rect, widget, event):
        self.label_chapter.set_text(f"{rect.caption}")

        e_x = event.x
        e_y = event.y

        # Set popover position
        self.popover_chapter.set_relative_to(widget)
        self.popover_chapter.set_pointing_to(rect)
        self.popover_chapter.set_position(Gtk.PositionType.TOP)
        self.popover_chapter.show_all()

        # Set current popover location and state
        # so that it is gets hiden only by clicking outside this point
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
            if rect.caption in self.user.list_mem_chapters:
                rect.paint_on()
            else:
                rect.paint_off()

        for rect in self.list_rects_pb:
            if rect.caption in self.user.list_mem_chapters:
                rect.paint_on()
            else:
                rect.paint_off()

    def _refresh_stats_label(self):

        pct_c = round(self.user.n_mem_chapters / self.book.n_chapters * 100, 2)
        pct_v = round(self.user.n_mem_verses   / self.book.n_verses   * 100, 2)
        pct_w = round(self.user.n_mem_words    / self.book.n_words    * 100, 2)
        pct_l = round(self.user.n_mem_letters  / self.book.n_letters  * 100, 2)

        stats_c = f"{self.user.n_mem_chapters}" + f" ({pct_c}%)"
        stats_v = f"{self.user.n_mem_verses}"   + f" ({pct_v}%)"
        stats_w = f"{self.user.n_mem_words}"    + f" ({pct_w}%)"
        stats_l = f"{self.user.n_mem_letters}"  + f" ({pct_l}%)"

        self.label_stats.set_markup(
            f"<span font='13'><b>Chapters: </b>{stats_c}</span>\n"
            f"<span font='13'><b>Verses: </b>{stats_v}</span>\n"
            f"<span font='13'><b>Words: </b>{stats_w}</span>\n"
            f"<span font='13'><b>Letters: </b>{stats_l}</span>"
        )
