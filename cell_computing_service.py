import random
import uuid

import protocol_pb2 as proto
import protocol_pb2_grpc as grpc_proto

import cis_env as env
from cis_cell import cells_consume_energy, cells_survive, cells_divide, random_dna, average_out_cell_energy
import cis_config as conf
import metrics
import cis_helper as helper


class CellComputeServicer(grpc_proto.CellInteractionServiceServicer):
    """
        Handles computation of cells.
    """

    COMPUTE_CELL_INTERACTION_HISTOGRAM = metrics.request_latency_histogram.labels("compute_cell_interactions")

    @COMPUTE_CELL_INTERACTION_HISTOGRAM.time()
    def ComputeCellInteractions(self, incoming_batch, context):
        """
            Computes the interaction of one batch of cells.
        """

        cell_batch = incoming_batch.cells_to_compute

        id_to_cell_dict = {}
        helper.map_cells_to_dict(cell_batch, id_to_cell_dict)
        helper.map_cells_to_dict(incoming_batch.cells_in_proximity, id_to_cell_dict)

        env.move_cells(
            cell_batch,
            id_to_cell_dict
        )

        env.feed_cells(
            cell_batch,
            incoming_batch.time_step
        )

        cells_consume_energy(cell_batch)

        living_cells = []
        living_cells = cells_survive(cell_batch)

        average_out_cell_energy(living_cells, id_to_cell_dict)

        cells_divide(living_cells)

        # format living_cells for protobuff
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

        for _ in range(big_bang_request.cell_amount):
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
                dna=random_dna(
                    min_length=big_bang_request.dna_length_range.min,
                    max_length=big_bang_request.dna_length_range.max,
                ),
                connections=[])

            yield cell
