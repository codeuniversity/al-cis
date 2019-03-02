import cis_config as conf
import random
import numpy as np
import dna_decoding
from cis_cell import random_vector_of_length
import scipy.constants as cons


def curl(pos, vec_len=0.004, coor_origin=conf.CURL_CENTRE):
    curl_pos = np.array([
        0,
        -pos.z + coor_origin[1],
        pos.y - coor_origin[2],
    ])
    return curl_pos * vec_len


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
    x = wave_function(cell_pos.x, time_step)
    y = wave_function(cell_pos.y, time_step)
    z = wave_function(cell_pos.z, time_step)

    return x + y + z


def wave_function(x, t, max_ampli=1, oscillation_period=1, init_deflection=0):
    """
        Classical mechanical wave function.
    """

    time_relation = t / oscillation_period
    space_relation = x / (cons.speed_of_light * oscillation_period)

    # sinput = sin + input
    sinput = 2 * np.pi * (time_relation - space_relation) + init_deflection

    return max_ampli * np.sin(sinput)


def get_value(dict, key):
    try:
        value = dict[key]
        return value, True
    except BaseException:
        return None, False


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


def average_out_energy_in_connected_cells(
        cell, cell_dict, already_averaged_dict):
    _, already_averaged = get_value(already_averaged_dict, cell.id)
    if already_averaged:
        return

    cell_group = group_connected_cells([cell], cell, cell_dict)
    energy_sum = 0
    for c in cell_group:
        energy_sum += c.energy_level

    for c in cell_group:
        c.energy_level = int(energy_sum / len(cell_group))
        already_averaged_dict[c.id] = True


def group_connected_cells(group, cell, cell_dict):
    for conn in cell.connections:
        other_cell, exists = get_value(cell_dict, conn.connected_to)
        if exists:
            if other_cell not in group:
                group.append(other_cell)
                group_connected_cells(group, other_cell, cell_dict)
    return group
