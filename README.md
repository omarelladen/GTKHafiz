<img height="64" src="data/icons/icon.png" align="left"/>

# GTKHafiz

GTKHafiz is a simple GTK 3 based app to track Qur'an memorization visually.

<p align="center" width="100%">
<img src="data/imgs/bars.png">
<img src="data/imgs/matrix.png">
<img src="data/imgs/list.png">
<img src="data/imgs/stats.png">
</p>

## Requirements
This GTK 3 based app uses [PyGObject](https://pygobject.gnome.org/), which is a Python package that provides bindings for GObject based libraries such as GTK, GStreamer, WebKitGTK, GLib, GIO and many more.

The dependencies usually come pre-installed on popular Linux distributions, however some do not come with the package 'python3-gi-cairo' installed by default.

To install it on Debian-based distributions:
```sh
sudo apt install python3-gi-cairo
```

If you wish to configure on other operating systems, including Windows, follow the instructions on the [PyGObject website](https://pygobject.gnome.org/getting_started.html), making sure to replace 'GTK4' with 'GTK3' when instaling packages.

## Install app
```sh
cd GTKHafiz
sudo scripts/install.sh
```
After the installation you can open the app with the apps menu of your desktop environment or run:
```sh
gtkhafiz
```

## Uninstall app
```sh
cd GTKHafiz
sudo scripts/uninstall.sh
```

## Credits
- Data source: [Quran Analysis](https://qurananalysis.com/analysis/basic-statistics.php?lang=EN)
- Inspiration: [ColorArabic](https://commons.wikimedia.org/wiki/File:ColorArabic.png)

