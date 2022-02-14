import csv
import numpy as np
import math

run = 2


if run == 1:
    with open('LEDs.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 2
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                print(row[0])
                line_count += 1
        print(f'Processed {line_count} lines.')
if run == 2:
    count = 0
    line = 1
    arrLED = np.zeros((29, 29))

    for point in range(29):
        for point2 in range(29):
            arrLED[point][point2] = None

    for coord_row in range(1, 30, 2):
        with open('LEDs.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                coord = row[coord_row]
                if coord == "extra":
                    line += 1
                # print(coord, coord.replace(" ", ""))
                coord = coord.replace(" ", "")
                coord = coord.split(",")
                # pin_LED = row[coord_row-1]
                # pin_LED = pin_LED.rsplit(" ")
                if coord[0].isdigit() and coord[1].isdigit():
                    pin = int(row[coord_row-1])
                    if line > 24:
                        pin += 24
                    #if coord_row > 1:
                    pin += 48 * math.floor(coord_row/2)
                    count += 1

                    arrLED[int(coord[0])-1][int(coord[1])-1] = pin
                    line += 1
                    if line > 48:
                        line = 1
    print(arrLED)
    print(count)

# print(np.where(arrLED == 502))
# # print(arrLED[25][11])
falseCount = 0

for i in range(0, 673):
    result = np.where(arrLED == i)
    print(i, result, bool(result[0].size > 0))
    if not bool(result[0].size > 0):
        falseCount += 1
    i += 1
print(falseCount)
# print(arrLED[20][10])

if run == 3:
    arr = np.zeros((29, 29))
    arr[1][1] = 1
    print(arr[1][1])
if run == 4:
    with open('LEDs.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line = 0
        for row in csv_reader:
            print(line)
            line += 1

#  + (48 * coord_row-1)