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
        """
            Computes the interaction of the whole batch of cells.
        """

        new_cells = []
        id_to_cell = {}
        id_to_cell_moved = {}
        id_combination_to_distance_checked = {}
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


        # Fighting
        for c in incoming_batch.cells_to_compute:
            cis_env.eat_closest_other_cell(c, incoming_batch.cells_to_compute, id_to_cell, id_combination_to_distance_checked)

        # Energy
        # Get Energy
        food_fac = conf.WANTED_CELL_AMOUNT_PER_BUCKET / len(incoming_batch.cells_to_compute)
        for c in incoming_batch.cells_to_compute:
            cis_env.feed(
                c,
                incoming_batch.time_step,
                food_factor=food_fac
            )

        # Consume Energy
        for c in incoming_batch.cells_to_compute:
            cis_cell.consume_energy(c)

        # Survival
        living_cells = []
        for c in incoming_batch.cells_to_compute:
            if cis_cell.is_alive(c):
                living_cells.append(c)

        # Average out energy in connected cells
        for c in living_cells:
            cis_env.average_out_energy_in_connected_cells(
                c,
                id_to_cell,
                id_to_cell_energy_averaged
            )

        # Division
        for c in living_cells:
            new_cell = cis_cell.divide(c)
            if new_cell is not None:
                living_cells.append(new_cell)

        new_batch = proto.CellComputeBatch(
            time_step=incoming_batch.time_step,
            cells_to_compute=living_cells,
            cells_in_proximity=incoming_batch.cells_in_proximity,
            batch_key=incoming_batch.batch_key,
        )
        return new_batch

    def BigBang(self, big_bang_request, context):
        """
            Creates batch of cells.
        """

        metrics.request_counter.labels("big_bang").inc()
        for i in range(big_bang_request.cell_amount):
            initial_position = []
            for j in conf.WORLD_DIMENSION:
                initial_position.append(random.uniform(0, j))
            initial_position = proto.Vector(
                x=random.uniform(big_bang_request.spawn_dimension.start.x, big_bang_request.spawn_dimension.end.x),
                y=random.uniform(big_bang_request.spawn_dimension.start.y, big_bang_request.spawn_dimension.end.y),
                z=random.uniform(big_bang_request.spawn_dimension.start.z, big_bang_request.spawn_dimension.end.z)
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
                ),
                connections=[])
            yield cell
