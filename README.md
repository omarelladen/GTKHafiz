<img height="64" src="imgs/icon.png" align="left"/>

# GTK Hafiz

GTK Hafiz is a simple GTK 3 app to track Qur'an memorization visually.

<p align="center" width="100%">
<img src="imgs/bars.png">
<img src="imgs/matrix.png">
<img src="imgs/list.png">
<img src="imgs/stats.png">
</p>

## Requirements
This GTK 3 app uses [PyGObject](https://pygobject.gnome.org/), which is a Python package that provides bindings for GObject based libraries such as GTK, GStreamer, WebKitGTK, GLib, GIO and many more.

The dependencies usually come pre-installed on popular Linux distributions with GUI, such as Debian, Mint and Fedora, except on newer versions of Ubuntu - which might not come with the 'python3-gi-cairo' package by default.

To install them on Debian-based distributions:
```sh
sudo apt install python3-gi python3-gi-cairo python3-cairo gir1.2-gtk-3.0
```
To configure on other operating systems, including Windows, follow the instructions on the [PyGObject website](https://pygobject.gnome.org/getting_started.html), making sure to replace 'GTK4' with 'GTK3' when instaling packages.

## Add desktop entry:
To launch the app directly from the desktop environment, there is a Shell script which after executed will add a desktop entry to ~/.local/share/applications/gtk-hafiz.desktop and also setup the scripts/launcher.sh that will be called to start the app.

To add the entry:
```sh
sh scripts/setup_desktop_entry.sh
```

You can also directly run:
```sh
sh scripts/launcher.sh
```
or:
```sh
python3 src/main.py
```

## Reset the database:
The database setup is done executing a Shell script that recreates the database and inserts the necessary CSV files from data/ using the sqlite3 CLI.

To install the sqlite3 CLI on Debian-based distributions:
```sh
sudo apt install sqlite3
```
Run the Shell Script:
```sh
sh scripts/setup_db.sh
```

## Credits
- Data source: [Quran Analysis](https://qurananalysis.com/analysis/basic-statistics.php?lang=EN)
- Inspiration: [ColorArabic](https://commons.wikimedia.org/wiki/File:ColorArabic.png)

