import os

from gi.repository import Gtk


class StatsExporter:
    def __init__(
            self,
            parent,
            title,
            default_filename="stats"
    ):
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

        stats = self.parent.label_stats.get_text()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self._save_string_to_file(
                stats,
                dialog.get_filename()
            )

        dialog.destroy()

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
            with open(path, "w") as f:
                f.write(content)
        except Exception as e:
            print(
                _("Failed to save file at '{path}': {e}").format(
                    path=path, e=e
                )
            )
