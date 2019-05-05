import random
import os
import uuid

import protocol_pb2 as proto

import cis.config as conf
import cis.dna_decoding as dna_decoding
from cis.helper import get_value, group_connected_cells, random_vector_of_length


# energy consumption
def cells_consume_energy(cells):

    for c in cells:
        consume_energy(c)


def consume_energy(cell):
    """
       Substracts the energy the cells consumes.
    """
    # general energy consumption
    if conf.GENERAL_ENERGY_CONSUMPTION < cell.energy_level:
        cell.energy_level -= conf.GENERAL_ENERGY_CONSUMPTION
    else:
        cell.energy_level = 0


# survival
def cells_survive(cells):

    survived_cells = []

    for c in cells:
        if is_alive(c):
            survived_cells.append(c)

    return survived_cells


def is_alive(cell):

    starvation_threshold = conf.ENERGY_THRESHOLD
    if cell.energy_level < starvation_threshold:
        return False
    else:
        return True


# average energy
def average_out_cell_energy(cells, cell_dict):

    map_id_to_cell_energy_averaged = {}

    for c in cells:
        average_out_energy_in_connected_cells(
            c,
            cell_dict,
            map_id_to_cell_energy_averaged
        )


def average_out_energy_in_connected_cells(cell, cell_dict, already_averaged_dict):

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


# division
def cells_divide(cells):

    for c in cells:
        new_cell = divide(c)
        if new_cell is not None:
            cells.append(new_cell)


def divide(cell):

    initial_energy = int(dna_decoding.initial_energy(cell.dna))
    cost = conf.DIVISION_ENERGY_COST + initial_energy
    if cell.energy_level > dna_decoding.division_treshold(cell.dna) + cost:
        cell.energy_level -= cost

        child_id = str(uuid.uuid1())
        child_connections = []

        if builds_connection_after_division(cell):
            child_connections.append(proto.Connection(connected_to=cell.id))
            conn = cell.connections.add()
            conn.connected_to = child_id

        child_dna = dna_decoding.mutate_dna_with_chance(
            dna_copy_or_sub_slice(cell),
            conf.MUTATION_CHANCE
        )

        new_cell = proto.Cell(
            id=child_id,
            energy_level=initial_energy,
            pos=randomly_shifted_pos(cell.pos, 10),
            vel=proto.Vector(
                x=0,
                y=0,
                z=0),
            dna=child_dna,
            connections=child_connections)
        return new_cell


def builds_connection_after_division(cell):
    return dna_decoding.builds_connection_after_division(
        cell.dna, len(cell.connections))


def dna_copy_or_sub_slice(cell):
    if dna_decoding.dna_should_sub_slice(cell.dna, len(cell.connections)):
        return dna_decoding.dna_sub_slice(cell.dna, len(cell.connections))
    return cell.dna


def randomly_shifted_pos(pos, shift_dist):
    d_x, d_y, d_z = random_vector_of_length(shift_dist)
    return proto.Vector(
        x=pos.x + d_x,
        y=pos.y + d_y,
        z=pos.z + d_z,
    )


def random_dna(min_length, max_length):
    return bytes(os.urandom(random.randint(min_length, max_length)))
