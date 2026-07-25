# Copyright 2025-2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import csv


exec(open("configs").read())


pb_line_width = 500  # total line length of juz'


n_lines = []
with open(LINES_FILE, mode="r") as file:
    reader = csv.reader(file)
    for line in reader:
        n_lines.append(line)

lines = []
with open(ORIG_BAR_SIZES_FILE, mode="r") as file:
    reader = csv.reader(file)
    for line in reader:
        value = float(line[2]) * pb_line_width / float(n_lines[int(line[0])-1][1])
        if len(line) == 4:
            line[3] = value
        else:
            line.append(value)
        lines.append(line)

with open(ORIG_BAR_SIZES_FILE, mode="w", newline="") as file:
    writer = csv.writer(file)
    for line in lines:
        writer.writerow(line)
