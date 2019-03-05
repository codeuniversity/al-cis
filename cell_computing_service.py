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
import metrics

import cis_env
import cis_cell


class CellComputeServicer(grpc_proto.CellInteractionServiceServicer):
    """
    """
    COMPUTE_CELL_INTERACTION_HISTOGRAM = metrics.request_latency_histogram.labels("compute_cell_interactions")

    @COMPUTE_CELL_INTERACTION_HISTOGRAM.time()
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

    def BigBang(self, request, context):
        metrics.request_counter.labels("big_bang").inc()
        for i in range(conf.INITIAL_NUMBER_CELLS):
            initial_position = []
            for j in conf.WORLD_DIMENSION:
                initial_position.append(random.uniform(0, j))
            initial_position = proto.Vector(
                x=initial_position[0],
                y=initial_position[1],
                z=initial_position[2])
            cell = proto.Cell(
                id=str(uuid.uuid1()),
                energy_level=conf.INITIAL_ENERGY_LEVEL,
                pos=initial_position,
                vel=proto.Vector(
                    x=0,
                    y=0,
                    z=0),
                dna=bytes(os.urandom(random.randint(3, 6))),
                connections=[])
            yield cell
