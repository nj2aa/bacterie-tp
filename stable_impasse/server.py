import grpc
import sys
import os
from concurrent import futures
from prometheus_client import start_http_server, Counter

sys.path.insert(0, '/app/proto')
import bacterie_pb2
import bacterie_pb2_grpc

TRAVERSE_COUNT = Counter('state_traversed_total', 'Nombre de traversees', ['state'])

class StableImpasseService(bacterie_pb2_grpc.BacterieServiceServicer):
    def Consume(self, request, context):
        TRAVERSE_COUNT.labels(state='stable_impasse').inc()
        return bacterie_pb2.ConsumeReply(
            next_state='stable_impasse',
            volume=request.volume,
            available_states=[]
        )

if __name__ == '__main__':
    start_http_server(8004)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bacterie_pb2_grpc.add_BacterieServiceServicer_to_server(StableImpasseService(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    print("Stable impasse server started on port 50054")
    server.wait_for_termination()
