import grpc
import sys
import os
from concurrent import futures
from prometheus_client import start_http_server, Counter

sys.path.insert(0, '/app/proto')
import bacterie_pb2
import bacterie_pb2_grpc

TRAVERSE_COUNT = Counter('state_traversed_total', 'Nombre de traversees', ['state'])

class StableService(bacterie_pb2_grpc.BacterieServiceServicer):
    def Consume(self, request, context):
        TRAVERSE_COUNT.labels(state='stable').inc()
        return bacterie_pb2.ConsumeReply(
            next_state='stable',
            volume=request.volume,
            available_states=['hypertrophie', 'atrophie']
        )

if __name__ == '__main__':
    start_http_server(8001)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bacterie_pb2_grpc.add_BacterieServiceServicer_to_server(StableService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Stable server started on port 50051")
    server.wait_for_termination()
