import sys
import cv2
from time import sleep
import numpy as np
sys.path.insert(1, '../')
import pykinect_azure as pykinect
import time
from termcolor import colored

from aaspi_tlc5947 import startAardvark, output_enable, output_disable, blast_bytes, aa_close

import csv
import numpy as np
import math


clearConsole = lambda: print('\n'* 4)

lednum = np.arange(29*29).reshape(29,29) #Actual array will be much more annoying to make




def square_update():
    start_time = time.time()
    print(colored('hello', 'red'), colored('world', 'green'))
    counter = 1
    usedled = []
    # print(lednum[14][14])42,183,202
    for i in range(29):
        for x in range(29):
            if 0 < resized[i][x][0] < 255 and not np.isnan(arrLED[i][x]):
                arrx[i][x] = " *"
                usedled.append(int(arrLED[i][x]))
            """
            if 0 < resized[i][x][0] == 202:
                arrx[i][x] = " _"
                # usedled.append(lednum[i][x])
                usedled.append(int(arrLED[i][x]))
            elif 0 < resized[i][x][2] == 202:
                arrx[i][x] = " _"
                # usedled.append(lednum[i][x])
                usedled.append(int(arrLED[i][x]))
            elif resized[i][x][0] != 202 and resized[i][x][0] != 255:
                arrx[i][x] = "||"
                # usedled.append(lednum[i][x])
                # usedled.append(int(arrLED[i][x]))
            elif resized[i][x][2] != 202 and resized[i][x][2] != 255:
                arrx[i][x] = "||"
                # usedled.append(lednum[i][x])
                # usedled.append(int(arrLED[i][x]))
            print(arrx[i][x], end=" ")
            if x % 29 == 0:
                print(" ")
            """

    usedLEDs = usedled
    print("\nUsed LEDs before before: ", usedLEDs)

    ##############################################################
    # Array Manipulation that will be gone in the real project
    # def isValidLED(num):
    #     if(0 < (num - 300) < 47):
    #         return True
    #     else:
    #         return False
    #
    # filteredLEDs = list(filter(isValidLED, usedLEDs))
    # print("Filtered list", list(filteredLEDs))
    # print("\nUsed LEDs before: ", usedLEDs)
    ##############################################################

    num_leds = 720
    # for i in range(num_leds):
    vals = [0] * num_leds
    for j in range(len(usedLEDs)):
        # # thing1 = filteredLEDs[j]
        # # print("Thing1 is ", thing1)
        # thing2 = arrLED[thing1 - 300]
        # print("Thing2 is ", thing2)
        # vals[thing2] = 30
        # # vals[arrLED[filteredLEDs[j] - 300]] = 30
        thing1 = usedLEDs[j]
        vals[thing1] = 30
    print("\nVals: ", vals)
    extendedVals = [0] * (720-num_leds)
    extendedVals.extend(vals)
    blast_bytes(handle, vals)


    #print("\nLED Array: ", resized)

    print("\n LEDs used:")
    print(usedled)
    # print(lednum[14][14])
    print(len(usedled), "total")




    run_time = time.time() - start_time
    print("Time: ", run_time)
    # print("Elapsed Time: ", delta_time)

    clearConsole()


pykinect.initialize_libraries(module_k4abt_path="/usr/lib/libk4abt.so", track_body=True)

# Modify camera configuration
device_config = pykinect.default_configuration
device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
# print(device_config)

# Start device
device = pykinect.start_device(config=device_config)

# Start body tracker
bodyTracker = pykinect.start_body_tracker()

cv2.namedWindow('Segmented Depth Image', cv2.WINDOW_NORMAL)


handle = startAardvark()
output_enable(handle)

#usedLEDs = [0, 1, 3, 14, 44]
# LEDs that are given as "used" from the body tracking program
#ledList = list(range(24, 36, +1)) + list(range(0, 12, +1)) + list(range(47, 35, -1)) + list(range(23, 11, -1))
# ledList = list(range(0, 12, +1)) + list(range(23, 11, -1))
# Formatted coordinates of the LED map

count = 0
line = 0
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
                pin = int(row[coord_row - 1])
                if line > 24:
                    pin += 24
                # if coord_row > 1:
                pin += 48 * math.floor(coord_row / 2)
                count += 1

                arrLED[int(coord[0]) - 1][int(coord[1]) - 1] = pin
                line += 1
                if line > 48:
                    line = 1



while True:
    k = cv2.waitKey(1)

    # Get capture
    capture = device.update()

    # Get body tracker frame
    body_frame = bodyTracker.update()

    # Get the color depth image from the capture
    ret, depth_color_image = capture.get_colored_depth_image()

    # Get the colored body segmentation
    ret, body_image_color = body_frame.get_segmentation_image()  # this is what we need

    # scale image
    scale_percent = 5.6640625  # percent of original size
    width = int(body_image_color.shape[1]* scale_percent / 100)
    height = int(body_image_color.shape[0]* scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(body_image_color, dim, interpolation=cv2.INTER_AREA)
    if not ret:
        continue
    # Overlay body segmentation on depth image
    cv2.imshow('Segmented Depth Image', resized)  # was body_image_color
    arrx = [
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
         "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "], ]
    resized = np.fliplr(resized)
    arrx = np.fliplr(arrx)

    square_update()
    if cv2.waitKey(1) == ord('q'):
        print("Closing Program")
        output_disable(handle)
        aa_close(handle)
        break
