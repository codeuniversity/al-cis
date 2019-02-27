import cis_config as conf
import random
import numpy as np
import dna_decoding
from cis_cell import random_vector_of_length


def curl(pos, vec_len=0.004, coor_origin=conf.CURL_CENTRE):
    curl_pos = np.array([
        0,
        -pos.z + coor_origin[1],
        pos.y - coor_origin[2],
    ])
    return curl_pos * vec_len


def feed_cell(cell, cell_dict, already_averaged_dict, food_factor=1):
    f = random.uniform(0, 1)
    if f < dna_decoding.food_theshold(cell.dna):
        cell.energy_level += int(dna_decoding.food_amount(cell.dna)
                                 * food_factor)
    if conf.GENERAL_ENERGY_CONSUMPTION < cell.energy_level:
        cell.energy_level -= conf.GENERAL_ENERGY_CONSUMPTION
    else:
        cell.energy_level = 0

    average_out_energy_in_connected_cells(
        cell, cell_dict, already_averaged_dict)


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
