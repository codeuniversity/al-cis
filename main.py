from concurrent import futures
import time
import logging
import numpy as np

import grpc

import protocol_pb2 as proto
import protocol_pb2_grpc as grpc_proto

import cis_config as config

def array_2_vec(array):
  return list_2_vec(array.tolist())

def list_2_vec(liste):
  assert len(liste) == 3
  return proto.Vector(x=liste[0],y=liste[1],z=liste[2])

class CellComputeServicer(grpc_proto.CellInteractionServiceServicer):
  def ComputeCellInteractions(self, request, context):
    #print(request.time_step, request.cells_to_compute, request.cells_in_proximity)
    return request
  def BigBang(self, request, context):
    for i in range(config.NUMBER_OF_INITIAL_CELLS):
      pos = np.random.rand(3) * config.WORLD_DIMENSIONS
      dna = bytes()
      c = proto.Cell(id=i, energy_level=20, pos=array_2_vec(pos), vel=list_2_vec([0,0,0]), dna=dna, connections=[])
      yield c

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  grpc_proto.add_CellInteractionServiceServicer_to_server(CellComputeServicer(), server)
  server.add_insecure_port('[::]:5000')
  server.start()
  try:
      while True:
          time.sleep(config._ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
      server.stop(0)


if __name__ == '__main__':
  logging.basicConfig()
  serve()

