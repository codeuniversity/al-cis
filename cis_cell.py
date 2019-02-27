# from cis_dna import
import cis_config as conf
import protocol_pb2 as proto
import uuid
import random
import math
import dna_decoding
import numpy as np


def move(cell):
    pass


def is_alive(cell):
    starvation_threshold = conf.ENERGY_THRESHOLD
    if cell.energy_level < starvation_threshold:
        return False
    else:
        return True


def builds_connection_after_division(cell):
    return dna_decoding.builds_connection_after_division(
        cell.dna, len(cell.connections))


def dna_copy_or_sub_slice(cell):
    if dna_decoding.dna_should_sub_slice(cell.dna, len(cell.connections)):
        return dna_decoding.dna_sub_slice(cell.dna, len(cell.connections))
    return cell.dna


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


def randomly_shifted_pos(pos, shift_dist):
    d_x, d_y, d_z = random_vector_of_length(shift_dist)
    return proto.Vector(
        x=pos.x + d_x,
        y=pos.y + d_y,
        z=pos.z + d_z,
    )


def random_vector_of_length(l):
    vec = np.random.uniform(1 / 10 * 6, 2, [3]) - 1
    dist = np.sqrt(vec.dot(vec))
    factor = l / dist
    return vec
