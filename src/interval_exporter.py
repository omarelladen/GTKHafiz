import os

from gi.repository import Gtk


class IntervalExporter:
    def __init__(self, parent, title, default_name, list_values):
        self.parent = parent
        self.title = title
        self.default_name = default_name
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
        dialog.set_current_name(f"{self.default_name}.txt")

        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        )

        self._add_file_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self._save_string_to_file(
                self._create_interval(),
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
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            print(f"Failed to save file at '{filename}': {e}")

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
