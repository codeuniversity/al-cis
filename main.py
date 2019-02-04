from concurrent import futures
import time
import logging

import grpc

import protocol_pb2 as proto
import protocol_pb2_grpc as grpc_proto

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class CellComputeServicer(grpc_proto.CellInteractionServiceServicer):
  def ComputeCellInteractions(self, request, context):
    print(request.time_step, request.cells_to_compute, request.cells_in_proximity)
    return request


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  grpc_proto.add_CellInteractionServiceServicer_to_server(CellComputeServicer(), server)
  server.add_insecure_port('[::]:5000')
  server.start()
  try:
      while True:
          time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
      server.stop(0)


if __name__ == '__main__':
  logging.basicConfig()
  serve()
