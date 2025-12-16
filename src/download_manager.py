import os

from gi.repository import Gtk

class DownloadManager:
    def __init__(self, parent):
        self.parent = parent

    def open_save_dialog(self):
        dialog = Gtk.FileChooserDialog(
            title="Save Progress Bars",
            parent=self.parent,
            transient_for=self.parent,
            action=Gtk.FileChooserAction.SAVE
        )
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_folder(os.path.expanduser("~"))
        dialog.set_current_name("progress.png")
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        )

        self._add_file_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            surface = self.parent.create_img()
            self._save_img_to_png(surface, dialog.get_filename())
            print(dialog.get_filename())

        dialog.destroy()

    def _add_file_filters(self, dialog):
        file_filter = Gtk.FileFilter()
        file_filter.set_name("PNG image")
        file_filter.add_mime_type("image/png")
        dialog.add_filter(file_filter)

        file_filter = Gtk.FileFilter()
        file_filter.set_name("Any files")
        file_filter.add_pattern("*")
        dialog.add_filter(file_filter)

    def _save_img_to_png(self, surface, filename):
        # Write the surface to a PNG file
        try:
            surface.write_to_png(filename)
            surface.finish()
        except Exception as e:
            print(f"Failed to save image at {filename}: {e}")
