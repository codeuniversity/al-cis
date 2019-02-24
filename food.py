import cis_config as conf
import numpy as np
import random


def feed_all_cells(cells, time):
    """
        Calc the amount of food a cell gets and add it to cell,
        given the position of the cell and the time.
    """
    new_cells = []

    for cell in cells:
        cell = feed(cell, time)
        cell = consume_energy(cell)
        if alive(cell):
            new_cells.append(cell)

    return new_cells


def feed(cell, time):
    """
        Give the cell food,
        depending on position and time.
    """
    if random.random() < conf.FOOD_THRESHOLD:
        cell.energy_level += conf.FOOD_ENERGY

    return cell


def consume_energy(cell):
    """
       Calc if cell still lives after energy consumption.
    """
    # general energy consumption
    cell.energy_level -= conf.GENERAL_ENERGY_CONSUMPTION

    # other energ consumption (in future)
    cell.energy_level -= 0

    return cell


def alive(cell):
    """
        Checks if cell is still living,
        depending on energy level.
    """
    if cell.energy_level > conf.ENERGY_THRESHOLD:
        return True

    return False
