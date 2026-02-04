#!/bin/sh

# Include config variables
. "$PWD"/config


echo "#!/usr/bin/python3

import sys
sys.path.insert(0, \"$DATA_DIR\")

from $APP_NAME_LOWER.main import main


if __name__ == \"__main__\":
    main()" > "$ORIG_BIN_FILE"
