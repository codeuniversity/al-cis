import numpy as np
import random

from cis_cell import random_vector_of_length, group_connected_cells
import cis_config as conf
import dna_decoding
from cis_helper import get_value


def curl(pos, vec_len=0.004, coor_origin=conf.CURL_CENTRE):
    curl_pos = np.array([
        0,
        -pos.z + coor_origin[1],
        pos.y - coor_origin[2],
    ])
    return curl_pos * vec_len


def feed_cells(cells, time_step):

    food_fac = conf.WANTED_CELL_AMOUNT_PER_BUCKET / len(cells)

    for c in cells:
        feed_cell(
            c,
            time_step,
            food_fac
        )


def feed_cell(cell, time_step, food_factor=1):
    """
        Give the cell food,
        depending on position and time_step.
    """

    #  get value from the food_function --> definition area: {-3, 3}
    food_value = food_function(cell.pos, time_step)

    # normalize food_value to {0, 1}
    food_value = normalize_food_value(food_value)

    # check if cell gets (the fixed amount of) food
    if food_value < dna_decoding.food_theshold(cell.dna):
        cell.energy_level += int(dna_decoding.food_amount(cell.dna) * food_factor)

    return cell


def normalize_food_value(num, definition_area_size=6):
    """
        Normalizes the definition area of the num to {0, 1} .
    """
    ret = num / definition_area_size + 0.5
    return ret


def food_function(cell_pos, time_step):
    """
        Creates the 4-dim food function and returns it.
    """
    x = wave_function(cell_pos.x, time_step)
    y = wave_function(cell_pos.y, time_step)
    z = wave_function(cell_pos.z, time_step)

    return x + y + z


def wave_function(x, t, max_ampli=1, oscillation_period=1, init_deflection=0):
    """
        Classical mechanical wave function.
    """

    time_relation = t / oscillation_period
    space_relation = x / (conf.WAVE_PROPAGATION * oscillation_period)

    # sinput = sin + input
    sinput = 2 * np.pi * (time_relation - space_relation) + init_deflection

    return max_ampli * np.sin(sinput)


def move_cells(cells, cell_dict):

    id_to_cell_moved_dict = {}

    for c in cells:
        move_cell_and_connected_cells(
            c, cell_dict, id_to_cell_moved_dict
        )


def move_cell_and_connected_cells(cell, cell_dict, moved_dict):
    global curl
    _value, moved = get_value(moved_dict, cell.id)
    if moved:
        return

    cell_group = group_connected_cells([cell], cell, cell_dict)
    # random movement for now, should be determined by dna and environment
    d_x, d_y, d_z = random_vector_of_length(4)
    mov_vec = random_vector_of_length(4)

    for g_cell in cell_group:
        mov_vec += curl(g_cell.pos)

    for g_cell in cell_group:
        g_cell_mov = mov_vec / len(cell_group)
        g_cell.pos.x += g_cell_mov[0]
        g_cell.pos.y += g_cell_mov[1]
        g_cell.pos.z += g_cell_mov[2]
        moved_dict[g_cell.id] = True
