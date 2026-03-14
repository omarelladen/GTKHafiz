# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import os

from gi.repository import Gtk


class ChapterExporter:
    def __init__(
            self,
            parent,
            title,
            list_values,
            default_filename="intervals"
    ):
        self.parent = parent
        self.title = title
        self.default_filename = default_filename
        self.funct_get_string = self._create_interval
        self.list_values = list_values

    def open_save_dialog(self):
        dialog = Gtk.FileChooserDialog(
            title=self.title,
            parent=self.parent,
            transient_for=self.parent,
            action=Gtk.FileChooserAction.SAVE
        )

        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_folder(os.path.expanduser("~"))
        dialog.set_current_name(f"{self.default_filename}.txt")

        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        )


        box = dialog.get_content_area()

        # Radio Buttons
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        padding_bt = 1

        bt = Gtk.RadioButton.new_with_label_from_widget(
            None, _("Intervals")
        )
        bt.connect(
            "toggled",
            self._on_bt_toggled,
            dialog,
            self._create_interval,
            "intervals"
        )
        hbox.pack_start(bt, False, False, padding_bt)

        bt = Gtk.RadioButton.new_from_widget(bt)
        bt.set_label(_("List"))
        bt.connect(
            "toggled",
            self._on_bt_toggled,
            dialog,
            self._create_list,
            "list"
        )
        hbox.pack_start(bt, False, False, padding_bt)

        box.pack_start(hbox, False, False, 0)
        dialog.show_all()


        self._add_file_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            string = self.funct_get_string()
            self._save_string_to_file(
                string,
                dialog.get_filename()
            )

        dialog.destroy()

    def _on_bt_toggled(self, button, dialog, funct, name):
        if button.get_active():
            self.funct_get_string = funct
            dialog.set_current_name(f"{name}.txt")

    def _add_file_filters(self, dialog):
        text_filter = Gtk.FileFilter()
        text_filter.set_name(_("Text Files"))
        text_filter.add_mime_type("text/plain")
        dialog.add_filter(text_filter)

        any_filter = Gtk.FileFilter()
        any_filter.set_name(_("All Files"))
        any_filter.add_pattern("*")
        dialog.add_filter(any_filter)

    def _save_string_to_file(self, content, path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            print(
                _("Failed to save file at '{path}': {e}").format(
                    path=path, e=e
                )
            )

    def _create_interval(self):
        if not self.list_values:
            return ""

        list_values_sorted = self.list_values
        list_values_sorted.sort()

        list_intervals = []
        start = list_values_sorted[0]
        end   = list_values_sorted[0]

        for value in list_values_sorted[1:]:
            if value == end + 1:
                # Continue current interval
                end = value
            else:
                # Close current interval
                if start == end:
                    list_intervals.append(str(start))
                else:
                    list_intervals.append(f"{start}-{end}")

                # Start new interval
                start = end = value

        # Add last interval
        if start == end:
            list_intervals.append(str(start))
        else:
            list_intervals.append(f"{start}-{end}")

        return ",".join(list_intervals)

    def _create_list(self):
        string_chapters = ""
        for chapter_number, checkbutton in self.parent.checkbuttons.items():
            if checkbutton.get_active():
                string_chapters += f"{checkbutton.get_label()}\n"
        return string_chapters
