# Copyright 2025-2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import gettext

from .app import App


def main(prefix):
    try:
        localedir = f"{prefix}/share/locale"
        gettext.install("gtkhafiz", localedir)

        app = App(prefix)
        app.parse_args()
        if app.setup():
            app.run()

    except Exception as e:
        print(_("Error starting application: {e}").format(e=e))


if __name__ == "__main__":
    main()
