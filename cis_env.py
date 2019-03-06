import cis_config as conf
import random
import numpy as np
import dna_decoding
import math
from cis_cell import random_vector_of_length


def curl(pos, vec_len=0.004, coor_origin=conf.CURL_CENTRE):
    curl_pos = np.array([
        0,
        -pos.z + coor_origin[1],
        pos.y - coor_origin[2],
    ])
    return curl_pos * vec_len


def feed(cell, time_step, food_factor=1):
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


def eat_other_cells(cell, other_cells, cell_dict, already_checked_dict):
    cell_group = group_connected_cells([cell], cell, cell_dict)
    for other_cell in other_cells:
        _value, already_checked = get_value(already_checked_dict, key_combination(other_cell.id, cell.id))
        if already_checked:
            next
        if in_distance(cell.pos, other_cell.pos, conf.CELL_EATING_DISTANCE):
            eat_both_ways(cell, other_cell)

        already_checked_dict[key_combination(cell.id, other_cell.id)] = True


def eat_both_ways(cell, other_cell):
    cell_eating_strength = dna_decoding.eating_strength(cell.dna, other_cell.dna)
    other_cell_eating_strength = dna_decoding.eating_strength(other_cell.dna, cell.dna)
    transfer_amount = int(cell_eating_strength - other_cell_eating_strength)
    cell.energy_level += transfer_amount
    other_cell.energy_level -= transfer_amount


def in_distance(pos, other_pos, distance):
    d_x = abs(pos.x - other_pos.x)
    if d_x > distance:
        return False
    d_y = abs(pos.y - other_pos.y)
    if d_y > distance:
        return False
    d_z = abs(pos.z - other_pos.z)
    if d_z > distance:
        return False

    return math.sqrt(d_x * d_x + d_y * d_y + d_z * d_z) < distance


def key_combination(id, other_id):
    return "{0}/{1}".format(id, other_id)
