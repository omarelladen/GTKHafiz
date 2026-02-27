import os
import re

from gi.repository import Gtk

from .import_dialog import ImportDialog


class IntervalImporter():
    def __init__(self, window, title):
        self.window = window
        self.title = title

    def run_dialog(self):
        list_values = []

        dialog = ImportDialog(self.window, self.title)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            text      = dialog.get_text()
            file_path = dialog.get_filename()

            if file_path:
                list_values = self._import_list_from_file(file_path)
            elif text:
                list_values = self._extract_values_list(text)

        dialog.destroy()

        return list_values

    def _extract_values_list(self, line):
        list_intevals = [i.strip() for i in line.split(",")]

        list_values = []
        for interval in list_intevals:
            re_match1 = re.match(r"(\d+)-(\d+)", interval)
            re_match2 = re.match(r"(\d+)",       interval)

            if re_match1:
                interval_start = int(re_match1.group(1))
                interval_end   = int(re_match1.group(2))

                if (interval_start == interval_end and
                    interval_start in range(1, 114+1)
                ):
                    list_values.append(interval_start)
                elif interval_start <= interval_end:
                    for i in range(interval_start, interval_end+1):
                        if 1 <= i <= 114:
                            list_values.append(i)
                elif interval_start > interval_end:
                    for i in range(interval_end, interval_start+1):
                        if 1 <= i <= 114:
                            list_values.append(i)
            elif re_match2:
                value = int(re_match2.group(1))
                if 1 <= value <= 114:
                    list_values.append(value)

        list_values = list(set(list_values))  # drop duplicates
        return list_values

    def _import_list_from_file(self, file):
        if os.path.isfile(file):
            try:
                with open(file, 'r') as f:
                    lines = f.readlines()

                if len(lines) < 1:
                    return None

                return self._extract_values_list(lines[0])

            except Exception as e:
                print(f"Failed to import from file '{file}': {e}")
                return None
        return None
