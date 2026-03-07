from setuptools import setup


config_file = "configs"

configs = {}
with open(config_file, "r") as f:
    exec(f.read(), configs)


app_name = configs.get("APP_NAME_LOWER")

data_files = [
    ("share/man/man1", [configs.get("ORIG_MAN_FILE")]),
    ("share/applications", [configs.get("ORIG_DESKTOP_FILE")]),
    ("share/icons/hicolor/64x64/apps", [configs.get("ORIG_ICON_FILE")]),
    (f"share/{app_name}", [
        config_file,
        configs.get("ORIG_DB_SCRIPT"),
        configs.get("ORIG_BAR_SIZES_FILE"),
        configs.get("ORIG_BOOKS_FILE"),
        configs.get("ORIG_CHAPTERS_FILE"),
    ]),
]

setup(
    name=configs.get("APP_NAME_LOWER"),
    version=configs.get("APP_VERSION"),
    package_dir={app_name: "src"},
    packages=[app_name],
    scripts=[configs.get("ORIG_BIN_FILE")],
    data_files=data_files,
)
