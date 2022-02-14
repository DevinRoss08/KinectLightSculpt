#!/usr/bin/env python3

# ==========================================================================
# IMPORTS
# ==========================================================================
from __future__ import division, with_statement, print_function
import sys

from aardvark_py import *
from pwm_converter import pwm_to_leds
from time import sleep
import time
# ==========================================================================
# CONSTANTS
# ==========================================================================
BUFFER_SIZE = 2048
SPI_BITRATE = 8000


# ==========================================================================
# FUNCTIONS
# ==========================================================================
def output_enable(handle):
    aa_gpio_set(handle, 0x00)


def output_disable(handle):
    aa_gpio_set(handle, 0x01)


def blast_bytes(handle, pwm_vals):
    # Write the data to the bus
    data_out = array('B', pwm_to_leds(pwm_vals))
    print("%s Data Elements %s" % (len(data_out), data_out))
    data_in = array_u08(len(data_out))
    (count, data_in) = aa_spi_write(handle, data_out, data_in)

    if count < 0:
        print("error: %s" % aa_status_string(count))
    elif count != len(data_out):
        print("error: only a partial number of bytes written")

    sys.stdout.write("Data written to device:")
    for i in range(count):
        if (i & 0x0f) == 0:
            sys.stdout.write("\n%04x:  " % i)

        sys.stdout.write("%02x " % (data_out[i] & 0xff))
        if ((i + 1) & 0x07) == 0:
            sys.stdout.write(" ")

    sys.stdout.write("\n\n")

    # Sleep a tad to make sure slave has time to process this request
    aa_sleep_ms(1)


# ==========================================================================
# MAIN PROGRAM
# ==========================================================================

def startAardvark():
    # Connect to the Aardvark
    port = 0
    mode = 2

    handle = aa_open(port)
    if handle <= 0:
        print("Unable to open Aardvark device on port %d" % port)
        print("Error code = %d" % handle)
        sys.exit()

    # Enable the Aardvark adapter's power supply.
    # This command is only effective on v2.0 hardware or greater.
    # The power pins on the v1.02 hardware are not enabled by default.
    aa_target_power(handle, AA_TARGET_POWER_BOTH)

    # Ensure that the SPI subsystem is enabled
    aa_configure(handle, AA_CONFIG_SPI_GPIO)

    # Ensure that GPIO pins are properly set up before blasting bytes
    aa_gpio_direction(handle, 0x01)
    aa_gpio_pullup(handle, 0x00)

    # Set up the clock phase
    aa_spi_configure(handle, mode >> 1, mode & 1, AA_SPI_BITORDER_MSB)

    # Set the bitrate
    bitrate = aa_spi_bitrate(handle, SPI_BITRATE)
    print("Bitrate set to %d kHz" % bitrate)
    return handle


if __name__ == "__main__":
    handle = startAardvark()
    usedLEDs = [0, 1, 3, 14, 44]
        # LEDs that are given as "used" from the body tracking program
    # ledList = list(range(24, 36, +1)) + list(range(0, 12, +1)) + list(range(12, 24, +1)) + list(range(36, 48, +1))
    ledList = list(range(24, 36, +1)) + list(range(0, 12, +1)) + list(range(47, 35, -1)) + list(range(23, 11, -1))
    # ledList = list(range(0, 12, +1)) + list(range(23, 11, -1))

    # Formatted coordinates of the LED map
    try:
        output_enable(handle)
        while True:
            num_leds = 48
            for i in range(num_leds):
                vals = [30] * num_leds
                # vals[i] = 30
                # vals[ledList[i]] = 0
                # for j in range(len(usedLEDs)):
                #     vals[ledList[usedLEDs[j]]] = 30
                #     print("Vals: ", vals)
                blast_bytes(handle, vals)
    finally:
        print("Closing Program")
        output_disable(handle)
        aa_target_power(handle, AA_TARGET_POWER_NONE)
        aa_close(handle)
