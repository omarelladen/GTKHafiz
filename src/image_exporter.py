# Copyright 2025-2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import os

from gi.repository import Gtk


class ImageExporter:
    def __init__(
            self,
            parent,
            title,
            default_filename="progress"
    ):
        self.parent = parent
        self.title = title
        self.default_filename = default_filename
        self.funct_create_img = self.parent.create_img_pb

    def open_save_dialog(self):
        dialog = Gtk.FileChooserDialog(
            title=self.title,
            parent=self.parent,
            transient_for=self.parent,
            action=Gtk.FileChooserAction.SAVE
        )
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_folder(os.path.expanduser("~"))
        dialog.set_current_name(f"{self.default_filename}.png")

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
            None, _("Progress Bars")
        )
        bt.connect(
            "toggled",
            self._on_bt_toggled,
            dialog,
            self.parent.create_img_pb,
            "progress"
        )
        hbox.pack_start(bt, False, False, padding_bt)

        bt = Gtk.RadioButton.new_from_widget(bt)
        bt.set_label(_("Matrix"))
        bt.connect(
            "toggled",
            self._on_bt_toggled,
            dialog,
            self.parent.create_img_matrix,
            "matrix"
        )
        hbox.pack_start(bt, False, False, padding_bt)

        box.pack_start(hbox, False, False, 0)
        dialog.show_all()


        self._add_file_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            surface = self.funct_create_img()
            self._save_img_to_png(surface, dialog.get_filename())

        dialog.destroy()

    def _on_bt_toggled(self, button, dialog, funct, name):
        if button.get_active():
            self.funct_create_img = funct
            dialog.set_current_name(f"{name}.png")

    def _add_file_filters(self, dialog):
        filefilter = Gtk.FileFilter()
        filefilter.set_name(_("PNG Images"))
        filefilter.add_mime_type("image/png")
        dialog.add_filter(filefilter)

        filefilter = Gtk.FileFilter()
        filefilter.set_name(_("All Files"))
        filefilter.add_pattern("*")
        dialog.add_filter(filefilter)

    def _save_img_to_png(self, surface, path):
        # Write the surface to a PNG file
        try:
            surface.write_to_png(path)
            surface.finish()
        except Exception as e:
            print(
                _("Failed to save file at '{path}': {e}").format(
                    path=path, e=e
                )
            )
