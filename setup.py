from setuptools import setup


config_file = "configs"

configs = {}
with open(config_file, "r") as f:
    exec(f.read(), configs)


app_name = configs.get("APP_NAME_LOWER")
keywords = configs.get("KEYWORDS").split(";")
pkg_dir = "src"

long_description_content_type = "text/markdown"
with open("README.md", "r") as f:
    lines = f.readlines()
filtered_lines = [ln for ln in lines if not ln.startswith("<")]  # rm tags
long_description = "".join(filtered_lines)


data_files = [
    ("share/man/man1",                 [configs.get("ORIG_MAN_FILE")]),
    ("share/applications",             [configs.get("ORIG_DESKTOP_FILE")]),
    ("share/icons/hicolor/64x64/apps", [configs.get("ORIG_ICON_FILE")]),
    (f"share/{app_name}", [
        config_file,
        configs.get("ORIG_BAR_SIZES_FILE"),
        configs.get("ORIG_BOOKS_FILE"),
        configs.get("ORIG_CHAPTERS_FILE"),
        configs.get("ORIG_DB_SCRIPT"),
    ]),
]

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
    keywords                      = keywords,
    license                       = configs.get("LICENSE"),
    package_dir                   = {app_name: pkg_dir},
    packages                      = [app_name],
    data_files                    = data_files,
    scripts                       = [configs.get("ORIG_BIN_FILE")],
)
