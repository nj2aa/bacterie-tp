import json
import os
import time

state_file = '/data/bacterie_state.json'

if not os.path.exists(state_file):
    with open(state_file, 'w') as f:
        json.dump({'state': 'stable', 'volume': 1.0}, f)
    print('State initialized')

while True:
    with open(state_file, 'r') as f:
        state = json.load(f)
    print(f"Current state: {state}")
    time.sleep(10)
