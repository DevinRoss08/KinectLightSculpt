# These functions are meant to convert human-readable pwm values to the corresponding byte code that TLC5947 accepts.

# Converts an integer to its 12-bit hex representation. These are the number of bits expected per channel on TLC5947.
def pwm_to_bytes(pwm: int) -> str:
    assert 0 <= pwm <= 4095, "PWM Value outside of accepted range"
    return "{:03X}".format(pwm)


# Converts list of PWM Values to their 12-bit hex representation and concatenates each value in an acceptable format
# for the Aardvark SPI Host Adapter.
def pwm_to_leds(pwm_vals: list):
    assert len(pwm_vals) % 24 == 0, "List of PWM Values does not align with number of LEDs on TLC5947"
    vals_in_hex = [pwm_to_bytes(val) for val in pwm_vals]

    joined_vals = ''.join(vals_in_hex)
    vals_in_bytes = [joined_vals[i:i+2] for i in range(0, len(joined_vals), 2)]

    vals_in_ints = [int(val, 16) for val in vals_in_bytes]
    print(f"Original vals: {pwm_vals} \nConverted vals: {vals_in_ints}")
    return vals_in_ints
