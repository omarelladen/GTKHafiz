# Copyright 2025-2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import os
import subprocess
from setuptools import setup
from setuptools.command.build_py import build_py


# Import config variables
config_file = "configs"
configs = {}
with open(config_file, "r") as f:
    exec(f.read(), configs)


app_name = configs.get("APP_NAME_LOWER")


# Get long description from README.md
long_description_content_type = "text/markdown"
with open("README.md", "r") as f:
    lines = f.readlines()
filtered_lines = [ln for ln in lines if not ln.startswith("<")]  # rm tags
long_description = "".join(filtered_lines)


# Map data files
def map_files(src_dir, ext):
    path_map = {}
    for root, dirs, files in os.walk(src_dir):
        clean_root = os.path.join(
            *(p for p in root.split(os.sep) if p and p != "build")
        )
        for file in files:
            if file.endswith(f".{ext}"):
                dst = os.path.join("share", clean_root)
                if dst not in path_map:
                    path_map[dst] = []
                path_map[dst].append(os.path.join(root, file))
    return list(path_map.items())

# Generate MO files
def gen_mo_files():
    cmd = [configs.get("MO_SCRIPT")]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError("Failed to generate MO files")

    mo_files  = map_files(configs.get("LOCALE_DIR"), "mo")
    return mo_files

class CustomBuildPy(build_py):
    def run(self):
        mo_files = gen_mo_files()
        self.distribution.data_files += mo_files

        super().run()


man_files = map_files(configs.get("MAN_DIR"), "1")

data_files = [
    ("share/applications",             [configs.get("ORIG_DESKTOP_FILE")]),
    ("share/icons/hicolor/64x64/apps", [configs.get("ORIG_ICON_FILE")]),
    (f"share/{app_name}", [
        config_file,
        configs.get("ORIG_BAR_SIZES_FILE"),
        configs.get("ORIG_BOOKS_FILE"),
        configs.get("ORIG_CHAPTERS_FILE"),
        configs.get("ORIG_DB_SCRIPT"),
    ]),
] + man_files


# PyPI Classifiers
classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Operating System :: POSIX",
    "Operating System :: POSIX :: Linux",
    "Environment :: X11 Applications :: GTK",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Topic :: Education",
    "Topic :: Religion",
]


setup(
    name                          = app_name,
    version                       = configs.get("APP_VERSION"),
    author                        = configs.get("AUTHOR"),
    author_email                  = configs.get("AUTHOR_EMAIL"),
    url                           = configs.get("WEBSITE_URL"),
    description                   = configs.get("DESCRIPTION"),
    long_description              = long_description,
    long_description_content_type = long_description_content_type,
    classifiers                   = classifiers,
    keywords                      = configs.get("KEYWORDS").split(";"),
    license                       = configs.get("LICENSE"),
    package_dir                   = {app_name: configs.get("PKG_DIR")},
    packages                      = [app_name],
    cmdclass                      = {"build_py": CustomBuildPy},
    data_files                    = data_files,
    scripts                       = [configs.get("ORIG_BIN_FILE")],
)
