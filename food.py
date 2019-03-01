import cis_config as conf
import numpy as np
import random
import scipy.constants as cons


def feed(cell, time_step):
    """
        Give the cell food,
        depending on position and time_step.
    """

    #  get value from the food_function --> definition area: {-3, 3}
    food_value = food_function(cell.pos, time_step)

    # normalize food_value to {0, 1}
    food_value = normalize(food_value)

    # check if cell gets (the fixed amount of) food
    if food_value < conf.FOOD_THRESHOLD:
        cell.energy_level += conf.FOOD_ENERGY

    return cell


def normalize(num, definition_area_size=6):
    """
        Normalizes the defenition area of the num to {0, 1} .
    """
    ret = round(num) / definition_area_size + 0.5
    return ret


def food_function(cell_pos, time_step):
    """
        Creates the 4-dim food function and returns it.
    """
    x = get_wave_function(cell_pos.x, time_step)
    y = get_wave_function(cell_pos.y, time_step)
    z = get_wave_function(cell_pos.z, time_step)

    return x + y + z


def wave_function(x, t, max_ampli=1, oscillation_period=1, init_deflection=0):
    """
        Classical mechanical wave function.
    """

    time_relation = t / oscillation_period
    space_relation = x / (cons.speed_of_light * oscillation_period)

    # sinput = sin + input
    sinput = 2 * np.pi * (time_relation - space_relation) + init_deflec

    return max_ampli * np.sin(sinput)
