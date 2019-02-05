import numpy as np
import grpc
import protocol_pb2 as proto
import protocol_pb2_grpc as grpc_proto
import cis_config as config
import random

def array_2_vec(array):
    return list_2_vec(array.tolist())

def list_2_vec(liste):
    assert len(liste) == 3
    return proto.Vector(x=liste[0],y=liste[1],z=liste[2])

def vec_2_array(vec):
    return np.array([vec.x,vec.y,vec.z])

def env_find_food(seed, time, pos):
    random.seed(seed)
    energy = random.randrange(0, config.MAX_FOOD_ENERGY)    
    return energy

def env_movement(seed, time, pos):
    random.seed(seed)
    x = random.randrange(0,config.MAX_VELOCITY)
    y = random.randrange(0,config.MAX_VELOCITY)
    z = random.randrange(0,config.MAX_VELOCITY)
    return np.array([x,y,z])

class CellComputeServicer(grpc_proto.CellInteractionServiceServicer):
    """
    """

    def ComputeCellInteractions(self, request, context):
        new_cell_batch = []
        # Move Cells
        for cell in request.cells_to_compute:
            new_pos = env_movement(config.MOV_SEED, request.time_step, cell.pos) + vec_2_array(cell.pos)
            cell.pos.x = new_pos[0]
            cell.pos.y = new_pos[1]
            cell.pos.z = new_pos[2]
        # Let Cells interact
        for cell in request.cells_to_compute:
            for _cell in request.cells_to_compute:
                if all(vec_2_array(_cell.pos) == vec_2_array(cell.pos)):
                    # interact
                    pass
            for _cell in request.cells_in_proximity:
                if all(vec_2_array(_cell.pos) == vec_2_array(cell.pos)):
                    # interact
                    pass
        # Feed Cells
        for cell in request.cells_to_compute:
            new_energy = env_find_food(config.FOOD_SEED, request.time_step, cell.pos) + cell.energy_level
            if new_energy < config.STARVATION_THRESHOLD:
                pass
            else:
                cell.energy_level = new_energy
                new_cell_batch.append(cell)
        response = proto.CellComputeBatch(time_step=request.time_step+1, cells_to_compute=new_cell_batch, cells_in_proximity=request.cells_in_proximity)
        return response

    def BigBang(self, request, context):
        global max_cell_id
        for i in range(config.NUMBER_OF_INITIAL_CELLS):
            pos = np.random.rand(3) * config.WORLD_DIMENSIONS
            dna = bytes()
            c = proto.Cell(id=i, energy_level=20, pos=array_2_vec(pos), vel=list_2_vec([0,0,0]), dna=dna, connections=[])
            yield c
        max_cell_id = i
