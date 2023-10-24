# colors.py
# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (211, 211, 211)
DARKSLATEGREY = (47, 79, 79)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MYGREEN = (0, 96, 65)
DARKORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
DARKGREEN = (0, 100, 0)
NAVY = (16, 22, 137)
LIGHTBLUE = (0, 113, 188)

import numpy as np


def convert_to_rgb(minimum, maximum, value):
    value = np.clip(value, minimum, maximum)
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value - minimum) / (maximum - minimum)
    b = int(max(0, 255 * (1 - ratio)))
    r = int(max(0, 255 * (ratio - 1)))
    g = 255 - b - r
    return (r, g, b)


def outdoor_temp_to_rgb(temperature):
    return convert_to_rgb(9, 35, temperature)


def indoor_temp_to_rgb(temperature):
    return convert_to_rgb(17, 27, temperature)


def temperature_to_rgb(temperature):
    # Define the temperature range and corresponding RGB colors
    temperature_range = [
        (6, (0, 0, 255)),  # 0°C: Blue
        (30, (255, 165, 0)),  # 30°C: Orange
        (40, (255, 0, 0)),
    ]  # 40°C: Red

    # Handle cases where the temperature is below 0°C or above 40°C
    if temperature <= 0:
        return (0, 0, 255)  # Blue
    elif temperature >= 40:
        return (255, 0, 0)  # Red

    # Iterate through the temperature range
    for i in range(len(temperature_range) - 1):
        low_temp, low_color = temperature_range[i]
        high_temp, high_color = temperature_range[i + 1]

        # Check if the temperature falls within this range
        if low_temp <= temperature < high_temp:
            # Linear interpolation between the two colors based on temperature
            t = (temperature - low_temp) / (high_temp - low_temp)
            r = int(low_color[0] + t * (high_color[0] - low_color[0]))
            g = int(low_color[1] + t * (high_color[1] - low_color[1]))
            b = int(low_color[2] + t * (high_color[2] - low_color[2]))

            return (r, g, b)

    return (0, 0, 0)  # Default: Black
