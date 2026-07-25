# Copyright 2025-2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import os
import sys
import gettext


def parse_args(exe_name, app_name, version):
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(_("Usage:"), end="\n")
        print(f"  {exe_name} ", end="")
        print(_("[OPTION…]"), end="\n\n")
        print(_("Help Options:"), end="\n")
        print("  -h, --help                 ", end="")
        print(_("Show help options"), end="\n\n")
        print(_("Application Options:"), end="\n")
        print("  -v, --version              ", end="")
        print(_("Print version information and exit"), end="\n\n")
        sys.exit(0)
    elif "--version" in args or "-v" in args:
        print(f"{app_name} {version}")
        sys.exit(0)

def main(exe_name, prefix):
    try:
        # Config variables
        configs = {}
        configs_path = os.path.join(prefix, "share", exe_name, "configs")
        with open(configs_path, "r") as f:
            exec(f.read(), configs)

        app_name= configs.get("APP_NAME")
        version = configs.get("APP_VERSION")

        localedir = os.path.join(prefix, "share", "locale")
        gettext.install(exe_name, localedir)

        parse_args(exe_name, app_name, version)

        from .app import App
        app = App(exe_name, prefix, configs)
        if app.setup():
            app.run()

    except Exception as e:
        print(_("Error starting application: {e}").format(e=e))
