import os

from gi.repository import Gtk


class StatsExporter:
    def __init__(self, parent, title, default_filename="stats"):
        self.parent = parent
        self.title = title
        self.default_filename = default_filename

    def open_save_dialog(self):
        dialog = Gtk.FileChooserDialog(
            title=self.title,
            parent=self.parent,
            transient_for=self.parent,
            action=Gtk.FileChooserAction.SAVE
        )

        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_folder(os.path.expanduser("~"))
        dialog.set_current_name(f"{self.default_filename}.yaml")

        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        )

        self._add_file_filters(dialog)

        stats = self.parent.calc_stats()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self._save_string_to_file(
                f"Chapters: {stats[0]}\n"
                f"Verses: {stats[1]}\n"
                f"Words: {stats[2]}\n"
                f"Letters: {stats[3]}\n",
                dialog.get_filename()
            )

        dialog.destroy()

    def _add_file_filters(self, dialog):
        text_filter = Gtk.FileFilter()
        text_filter.set_name("Text Files")
        text_filter.add_mime_type("text/plain")
        dialog.add_filter(text_filter)

        any_filter = Gtk.FileFilter()
        any_filter.set_name("Any Files")
        any_filter.add_pattern("*")
        dialog.add_filter(any_filter)

    def _save_string_to_file(self, content, filename):
        try:
            with open(filename, "w") as f:
                f.write(content)
        except Exception as e:
            print(f"Failed to save file at '{filename}': {e}")
