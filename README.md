<img height="64" src="data/icons/gtkhafiz.png" align="left"/>

# GTKHafiz

GTKHafiz is a simple GTK3-based app to track Quran memorization visually.
After selecting which chapters he has memorized, the user can see his progress
represented by colored rectangles, each one corresponding to a chapter.
The app also shows global statistics about it.

<p align="center" width="100%">
<img src="data/imgs/bars.png">
<img src="data/imgs/matrix.png">
<img src="data/imgs/list.png">
<img src="data/imgs/stats.png">
<img src="data/imgs/menu.png">
</p>

## Requirements
The dependencies usually come pre-installed on popular Linux distributions,
however some do not come with the package python3-gi-cairo installed by default.

To install all dependencies on Debian:
```sh
sudo apt install gir1.2-gtk-3.0 python3-gi python3-gi-cairo
```

To configure on other operating systems, including Windows, follow the instructions
on the [PyGObject website](https://pygobject.gnome.org/getting_started.html),
making sure to replace the GTK 4 packages with the corresponding GTK 3 ones on installation.

## Install the app on Linux
```sh
sudo scripts/install.sh
```
After installing, you can launch the app from the application menu of your
desktop environment or run:
```sh
gtkhafiz
```

## Uninstall the app
```sh
sudo scripts/uninstall.sh
```

## Credits
- Data source: [Quran Analysis](https://qurananalysis.com/analysis/basic-statistics.php?lang=EN)
- Inspiration: [ColorArabic](https://commons.wikimedia.org/wiki/File:ColorArabic.png)
