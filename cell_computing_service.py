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
import uuid

import cis_env
import cis_cell


class CellComputeServicer(grpc_proto.CellInteractionServiceServicer):
    """
    """

    def ComputeCellInteractions(self, incoming_batch, context):
        new_cells = []
        id_to_cell = {}
        id_to_cell_moved = {}
        id_to_cell_energy_averaged = {}
        for c in incoming_batch.cells_to_compute:
            id_to_cell[c.id] = c
        for c in incoming_batch.cells_in_proximity:
            id_to_cell[c.id] = c

        # Movement
        for c in incoming_batch.cells_to_compute:
            cis_env.move_cell_and_connected_cells(
                c, id_to_cell, id_to_cell_moved)
        # Interaction

        # Energy
        for c in incoming_batch.cells_to_compute:
            cis_env.feed_cell(
                c,
                id_to_cell,
                id_to_cell_energy_averaged,
                food_factor=conf.WANTED_CELL_AMOUNT_PER_BUCKET /
                len(
                    incoming_batch.cells_to_compute))

        # Survival
        living_cells = []
        for c in incoming_batch.cells_to_compute:
            if cis_cell.is_alive(c):
                living_cells.append(c)

        # Division
        for c in living_cells:
            new_cell = cis_cell.divide(c)
            if new_cell is not None:
                living_cells.append(new_cell)

        new_batch = proto.CellComputeBatch(
            time_step=incoming_batch.time_step,
            cells_to_compute=living_cells,
            cells_in_proximity=incoming_batch.cells_in_proximity,
        )
        return new_batch

    def BigBang(self, big_bang_request, context):
        for i in range(big_bang_request.cell_amount):
            initial_position = proto.Vector(
                x=random.uniform(big_bang_request.start.x, big_bang_request.end.x),
                y=random.uniform(big_bang_request.start.y, big_bang_request.end.y),
                z=random.uniform(big_bang_request.start.z, big_bang_request.end.z)
            )

            cell = proto.Cell(
                id=str(uuid.uuid1()),
                energy_level=big_bang_request.energy_level,
                pos=initial_position,
                vel=proto.Vector(
                    x=0,
                    y=0,
                    z=0),
                dna=cis_cell.random_dna(
                    min_length=big_bang_request.dna_length_range.min,
                    max_length=big_bang_request.dna_length_range.max,
                )
                connections=[])
            yield cell
