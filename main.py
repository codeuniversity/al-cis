from concurrent import futures
import time
import logging
import grpc
import protocol_pb2_grpc as grpc_proto

from cell_computing_service import CellComputeServicer
import cis_config as config

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

