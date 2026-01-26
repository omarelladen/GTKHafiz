import os

from gi.repository import Gtk


class ImportDialog(Gtk.Dialog):
    def __init__(self, parent, title):
        super().__init__(
            title=title,
            parent=parent,
            transient_for=parent,
            modal=True
        )

        self.set_default_size(300, 100)

        box = self.get_content_area()
        box.set_spacing(10)

        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK,     Gtk.ResponseType.OK)


        # File Chooser Button
        self.file_chooser_button = Gtk.FileChooserButton(
            title="Import From File",
            action=Gtk.FileChooserAction.OPEN
        )
        self.file_chooser_button.set_current_folder(os.path.expanduser("~"))
        box.pack_start(self.file_chooser_button, False, False, 0)

        self._add_file_filters()

        # Or text
        label_or = Gtk.Label(label="or")
        box.pack_start(label_or, False, False, 0)

        # Text Entry
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("e.g. 2-6, 9, 12-16")
        box.pack_start(self.entry, False, False, 0)

        self.show_all()

    def _add_file_filters(self):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        self.file_chooser_button.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        self.file_chooser_button.add_filter(filter_any)

    def get_text(self):
        return self.entry.get_text()

    def get_filename(self):
        return self.file_chooser_button.get_filename()
