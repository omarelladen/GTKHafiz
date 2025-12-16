import os

from gi.repository import Gtk

class ImportDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(
            title="Import Chapter Intervals",
            parent=parent,
            transient_for=parent,
            modal=True
        )

        self.set_default_size(300, 100)

        box = self.get_content_area()
        box.set_spacing(10)

        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)


        # File Chooser Button
        self.file_chooser_button = Gtk.FileChooserButton(
            title="Import from file",
            action=Gtk.FileChooserAction.OPEN
        )
        self.file_chooser_button.set_current_folder(os.path.expanduser("~"))
        box.pack_start(self.file_chooser_button, False, False, 0)

        self._add_file_filters()

        # Or text
        or_label = Gtk.Label(label="or")
        box.pack_start(or_label, False, False, 0)

        # Text Entry
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("e.g. 2-6, 9, 12-16")
        box.pack_start(self.entry, False, False, 0)

        self.show_all()

    def _add_file_filters(self):
        text_filter = Gtk.FileFilter()
        text_filter.set_name("Text files")
        text_filter.add_mime_type("text/plain")
        self.file_chooser_button.add_filter(text_filter)

        any_filter = Gtk.FileFilter()
        any_filter.set_name("Any files")
        any_filter.add_pattern("*")
        self.file_chooser_button.add_filter(any_filter)

    def get_text(self):
        return self.entry.get_text()

    def get_filename(self):
        return self.file_chooser_button.get_filename()
