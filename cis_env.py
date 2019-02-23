import cis_config as conf
import random
import numpy as np
import dna_decoding

class Curl():
    def __init__(self, coor_origin, vec_len):
        self.coor_origin = coor_origin
        self.vec_len = vec_len

    def _P(self, x, y, z):
        nx = 0
        return nx

    def _Q(self, x, y, z):
        ny = -z + self.coor_origin[1]
        return ny

    def _R(self, x, y, z):
        nz = y - self.coor_origin[2]
        return nz

    def get(self, x, y, z):
        old_pos = np.array([x, y, z])
        curl_pos = np.array([
            self._P(x, y, z),
            self._Q(x, y, z),
            self._R(x, y, z),
        ])

        return curl_pos * self.vec_len


curl = Curl(
    np.array([
        conf.WORLD_DIMENSION[0] / 2,
        conf.WORLD_DIMENSION[1] / 2,
        conf.WORLD_DIMENSION[2] / 2
    ]),
    0.002
)

def feed_cell(cell, cell_dict, already_averaged_dict, food_factor=1):
    f = random.uniform(0, 1)
    if f < dna_decoding.food_theshold(cell.dna):
        cell.energy_level += int(dna_decoding.food_amount(cell.dna) * food_factor)

    cell.energy_level -= conf.GENERAL_ENERGY_CONSUMPTION
    average_out_energy_in_connected_cells(
        cell, cell_dict, already_averaged_dict)

def get_value(dict, key):
    try:
        value = dict[key]
        return value, True
    except:
        return None, False


def move_cell_and_connected_cells(cell, cell_dict, moved_dict):
    global curl

    _value, moved = get_value(moved_dict, cell.id)
    if moved:
        return

    cell_group = group_connected_cells([cell], cell, cell_dict)
    d_x = 0
    d_y = 0
    d_z = 0

    for g_cell in cell_group:
        new_pos = curl.get(cell.pos.x, cell.pos.y, cell.pos.z)
        d_x += new_pos[0] - cell.pos.x
        d_y += new_pos[1] - cell.pos.y
        d_z += new_pos[2] - cell.pos.z

    for g_cell in cell_group:
        g_cell.pos.x += d_x / len(cell_group)
        g_cell.pos.y += d_y / len(cell_group)
        g_cell.pos.z += d_z / len(cell_group)
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
