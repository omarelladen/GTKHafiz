#!/bin/sh

# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

# Include config variables
. "$PWD"/configs


echo "#!/usr/bin/python3

import os

from $APP_NAME_LOWER.main import main


if __name__ == \"__main__\":
    prefix = os.path.dirname(__file__).replace(\"/bin\", \"\")
    main(prefix)" > "$ORIG_BIN_FILE"
