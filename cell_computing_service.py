import numpy as np
import grpc
import protocol_pb2 as proto
import protocol_pb2_grpc as grpc_proto
import cis_config as conf
import random
import time
import dna_decoding
import os
import math
cell_id_counter = 0


class CellComputeServicer(grpc_proto.CellInteractionServiceServicer):
    """
    """

    def ComputeCellInteractions(self, incoming_batch, context):
        global cell_id_counter
        new_cells = []
        id_to_cell = {}
        id_to_cell_moved = {}
        id_to_cell_energy_averaged = {}
        for c in incoming_batch.cells_to_compute:
            id_to_cell[str(c.id)] = c
        for c in incoming_batch.cells_in_proximity:
            id_to_cell[str(c.id)] = c

        # Movement
        for c in incoming_batch.cells_to_compute:
            move_cell_and_connected_cells(c, id_to_cell, id_to_cell_moved)
        # Interaction

        # Energy
        for c in incoming_batch.cells_to_compute:
            f = random.uniform(0, 1)
            if f < dna_decoding.food_theshold(c.dna):
                food_factor = conf.WANTED_CELL_AMOUNT_PER_BUCKET / \
                    len(incoming_batch.cells_to_compute)
                c.energy_level += int(dna_decoding.food_amount(c.dna) * food_factor)

            c.energy_level -= conf.GENERAL_ENERGY_CONSUMPTION
            average_out_energy_in_connected_cells(
                c, id_to_cell, id_to_cell_energy_averaged)

            if c.energy_level > conf.ENERGY_THRESHOLD:
                new_cells.append(c)

        # Division
        for c in incoming_batch.cells_to_compute:
            initial_energy = int(dna_decoding.initial_energy(c.dna))
            cost = conf.DIVISION_ENERGY_COST + initial_energy
            if c.energy_level > dna_decoding.division_treshold(c.dna) + cost:
                c.energy_level -= cost

                child_id = conf.INITIAL_NUMBER_CELLS + cell_id_counter
                child_connections = []

                if dna_decoding.builds_connection_after_division(
                    c.dna,
                    len(c.connections),
                ):
                    child_connections.append(proto.Connection(connected_to=c.id))
                    conn = c.connections.add()
                    conn.connected_to=child_id
                    print("++conn++")
                child_dna = None
                if dna_decoding.should_sub_slice(c.dna, len(c.connections)):
                    dna_decoding.dna_sub_slice(c.dna, len(c.connections))
                else:
                    child_dna = c.dna

                child_dna = dna_decoding.mutate_dna_with_chance(
                    c.dna,
                    conf.MUTATION_CHANCE
                )

                nc = proto.Cell(
                    id=child_id,
                    energy_level=initial_energy,
                    pos=randomly_shifted_pos(c.pos, 10),
                    vel=proto.Vector(
                        x=0,
                        y=0,
                        z=0),
                    dna=child_dna,
                    connections=child_connections)
                cell_id_counter += 1
                new_cells.append(nc)

        new_batch = proto.CellComputeBatch(
            time_step=incoming_batch.time_step,
            cells_to_compute=new_cells,
            cells_in_proximity=incoming_batch.cells_in_proximity,
        )
        # time.sleep(0.05)
        return new_batch

    def BigBang(self, request, context):
        for i in range(conf.INITIAL_NUMBER_CELLS):
            initial_position = []
            for j in conf.WORLD_DIMENSION:
                initial_position.append(random.uniform(0, j)+800)
            initial_position = proto.Vector(
                x=initial_position[0],
                y=initial_position[1],
                z=initial_position[2])
            cell = proto.Cell(
                id=i,
                energy_level=conf.INITIAL_ENERGY_LEVEL,
                pos=initial_position,
                vel=proto.Vector(
                    x=0,
                    y=0,
                    z=0),
                dna=bytes(os.urandom(random.randint(3, 6))),
                connections=[])
            yield cell


def get_value(dict, key):
    try:
        value = dict[str(key)]
        return value, True
    except:
        return None, False


def move_cell_and_connected_cells(cell, cell_dict, moved_dict):
    _value, moved = get_value(moved_dict, cell.id)
    if moved:
        return

    d_x = random.uniform(-conf.WORLD_VELOCITY, conf.WORLD_VELOCITY)
    d_y = random.uniform(-conf.WORLD_VELOCITY, conf.WORLD_VELOCITY)
    d_z = random.uniform(-conf.WORLD_VELOCITY, conf.WORLD_VELOCITY)

    cell_group = group_connected_cells([cell], cell, cell_dict)
    for g_cell in cell_group:
        g_cell.pos.x += d_x
        g_cell.pos.y += d_y
        g_cell.pos.z += d_z
        moved_dict[str(g_cell.id)] = True


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
        already_averaged_dict[str(c.id)] = True


def group_connected_cells(group, cell, cell_dict):
    for conn in cell.connections:
        other_cell, exists = get_value(cell_dict, conn.connected_to)
        if exists:
            if other_cell not in group:
                group.append(other_cell)
                group_connected_cells(group, other_cell, cell_dict)
    return group

def randomly_shifted_pos(pos, shift_dist):
    d_x, d_y, d_z = random_vector_of_length(shift_dist)
    return proto.Vector(
        x=pos.x + d_x,
        y=pos.y + d_y,
        z=pos.z + d_z,
    )


def random_vector_of_length(l):
    x = random.uniform(1 / 10 * 3, 1)
    y = random.uniform(1 / 10 * 3, 1)
    z = random.uniform(1 / 10 * 3, 1)
    # x = 1
    # y = 0
    # z = 0
    dist = math.sqrt(x * x + y * y + z * z)
    factor = l / dist
    return x * factor, y * factor, z * factor
