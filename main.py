from concurrent import futures
import time
import logging
import grpc
import protocol_pb2_grpc as grpc_proto
import protocol_pb2 as proto

from cell_computing_service import CellComputeServicer
import cis_config as config


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_proto.add_CellInteractionServiceServicer_to_server(
        CellComputeServicer(), server)
    server.add_insecure_port('[::]:5000')
    server.start()

    channel = grpc.insecure_channel('localhost:3000')
    stub = grpc_proto.SlaveRegistrationServiceStub(channel)
    stub.Register(proto.SlaveRegistration(address="localhost:5000", threads=4))

    try:
        while True:
            time.sleep(config._ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
