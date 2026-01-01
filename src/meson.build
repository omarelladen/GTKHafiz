configure_file(
  input: 'main.py',
  output: 'gtkhafiz',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
)

# Python sources
sources = [
  '__init__.py',
  'app.py',
  'book.py',
  'chapter.py',
  'chapter_rectangle.py',
  'color_utils.py',
  'db_manager.py',
  'download_manager.py',
  'import_dialog.py',
  'import_manager.py',
  'main.py',
  'preferences_manager.py',
  'user.py',
  'window.py',
]
# Install sources
install_data(sources, install_dir: moduledir)

install_subdir('utils', install_dir: moduledir)
install_subdir('lib', install_dir: moduledir)
install_subdir('widgets', install_dir: moduledir)

if profile == 'development'
  install_subdir('tests', install_dir: moduledir)
endif
