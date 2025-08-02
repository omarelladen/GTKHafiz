import csv

pb_line_width = 500  # total line length of juz'

exec(open('config').read())

n_lines = []
with open('data/lines.csv', mode='r') as file:
    reader = csv.reader(file)
    for line in reader:
        n_lines.append(line)

lines = []
with open(BAR_SIZES_FILE, mode='r') as file:
    reader = csv.reader(file)
    for line in reader:
        value = float(line[2]) * pb_line_width / float(n_lines[int(line[0])-1][1])
        if len(line) == 4:
            line[3] = value
        else:
            line.append(value)

        lines.append(line)

with open(BAR_SIZES_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    for line in lines:
        writer.writerow(line)