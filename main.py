from concurrent import futures
import time
import logging
import grpc
import protocol_pb2_grpc as grpc_proto
import protocol_pb2 as proto
import os
import prometheus_client

from cis.cell_computing_service import CellComputeServicer as CIS
import cis.config as conf


def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    grpc_proto.add_CellInteractionServiceServicer_to_server(
        CIS(),
        server
    )

    server.add_insecure_port('[::]:' + os.environ['GRPC_PORT'])

    server.start()

    channel = grpc.insecure_channel(os.environ['MASTER_ADDRESS'])
    stub = grpc_proto.SlaveRegistrationServiceStub(channel)
    stub.Register(
        proto.SlaveRegistration(
            address="{}:{}".format(os.environ['HOST'], os.environ['GRPC_PORT']),
            threads=1
        )
    )

    try:
        while True:
            time.sleep(conf._ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    prometheus_client.start_http_server(int(os.environ['PROMETHEUS_PORT']))
    serve()
