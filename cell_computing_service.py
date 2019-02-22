import numpy as np
import grpc
import protocol_pb2 as proto
import protocol_pb2_grpc as grpc_proto
import cis_config as conf
import random
import time
import uuid


class CellComputeServicer(grpc_proto.CellInteractionServiceServicer):
    """
    """

    def ComputeCellInteractions(self, incoming_batch, context):
        new_cells = []
        # Movement
        for c in incoming_batch.cells_to_compute:
            c.pos.x += random.uniform(-conf.WORLD_VELOCITY,
                                      conf.WORLD_VELOCITY)
            c.pos.y += random.uniform(-conf.WORLD_VELOCITY,
                                      conf.WORLD_VELOCITY)
            c.pos.z += random.uniform(-conf.WORLD_VELOCITY,
                                      conf.WORLD_VELOCITY)
        # Interaction

        # Energy
        for c in incoming_batch.cells_to_compute:
            f = random.uniform(0, 1)
            if f < conf.FOOD_THRESHOLD:
                c.energy_level += conf.FOOD_ENERGY

            c.energy_level -= conf.GENERAL_ENERGY_CONSUMPTION
            if c.energy_level > conf.ENERGY_THRESHOLD:
                new_cells.append(c)

        # Division
        for c in incoming_batch.cells_to_compute:
            if c.energy_level > conf.DIVISION_THRESHOLD:
                c.energy_level -= conf.DIVISION_ENERGY_COST

                nc = proto.Cell(
                    id=str(uuid.uuid1()),
                    energy_level=conf.INITIAL_ENERGY_LEVEL,
                    pos=c.pos,
                    vel=proto.Vector(
                        x=0,
                        y=0,
                        z=0),
                    dna=bytes(),
                    connections=[])
                new_cells.append(nc)

        new_batch = proto.CellComputeBatch(
            time_step=incoming_batch.time_step,
            cells_to_compute=new_cells,
            cells_in_proximity=incoming_batch.cells_in_proximity,
        )
        # time.sleep(0.1)
        return new_batch

    def BigBang(self, request, context):
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
                dna=bytes(),
                connections=[])
            yield cell
