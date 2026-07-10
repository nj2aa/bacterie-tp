import grpc
import sys
import os
import time
from concurrent import futures
from prometheus_client import start_http_server, Counter

sys.path.insert(0, '/app/proto')
import bacterie_pb2
import bacterie_pb2_grpc

TRAVERSE_COUNT = Counter('state_traversed_total', 'Nombre de traversees', ['state'])

last_update = time.time()

class HypertrophieService(bacterie_pb2_grpc.BacterieServiceServicer):
    def Consume(self, request, context):
        global last_update
        TRAVERSE_COUNT.labels(state='hypertrophie').inc()
        volume = request.volume
        if time.time() - last_update >= 10:
            volume = volume * 1.10
            last_update = time.time()
        return bacterie_pb2.ConsumeReply(
            next_state='hypertrophie',
            volume=volume,
            available_states=['stable']
        )

if __name__ == '__main__':
    start_http_server(8002)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bacterie_pb2_grpc.add_BacterieServiceServicer_to_server(HypertrophieService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Hypertrophie server started on port 50052")
    server.wait_for_termination()
