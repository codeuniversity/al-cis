# from cis_dna import
import cis_config as conf
import protocol_pb2 as proto
import uuid


def move(cell):
    pass


def is_alive(cell):
    starvation_threshold = conf.ENERGY_THRESHOLD
    if cell.energy_level < starvation_threshold:
        return False
    else:
        return True


def divide(cell):
    if cell.energy_level > conf.DIVISION_THRESHOLD:
        energy_transfer = conf.DIVISION_ENERGY_COST

        cell.energy_level -= energy_transfer
        nc = proto.Cell(
            id=str(uuid.uuid1()),
            energy_level=energy_transfer,
            pos=cell.pos,
            vel=proto.Vector(
                x=0,
                y=0,
                z=0),
            dna=bytes(),
            connections=[])
        return nc
