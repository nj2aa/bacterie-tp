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

class AtrophieService(bacterie_pb2_grpc.BacterieServiceServicer):
    def Consume(self, request, context):
        global last_update
        TRAVERSE_COUNT.labels(state='atrophie').inc()
        volume = request.volume
        if time.time() - last_update >= 10:
            volume = volume * 0.95
            last_update = time.time()
        available = ['stable']
        if volume <= 0:
            available = ['stable', 'stable_impasse']
        return bacterie_pb2.ConsumeReply(
            next_state='atrophie',
            volume=volume,
            available_states=available
        )

if __name__ == '__main__':
    start_http_server(8003)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bacterie_pb2_grpc.add_BacterieServiceServicer_to_server(AtrophieService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Atrophie server started on port 50053")
    server.wait_for_termination()
