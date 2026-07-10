import grpc
import sys
import os
from flask import Flask, render_template_string, request, redirect

sys.path.insert(0, '/app/proto')
import bacterie_pb2
import bacterie_pb2_grpc

app = Flask(__name__)

STATE_PORTS = {
    'stable': 50051,
    'hypertrophie': 50052,
    'atrophie': 50053,
    'stable_impasse': 50054
}

bacterie = {
    'state': 'stable',
    'volume': 1.0
}

def call_state(state, volume):
    port = STATE_PORTS[state]
    host = os.environ.get(f'{state.upper()}_HOST', 'localhost')
    with grpc.insecure_channel(f'{host}:{port}') as channel:
        stub = bacterie_pb2_grpc.BacterieServiceStub(channel)
        response = stub.Consume(bacterie_pb2.ConsumeRequest(
            original_state=state,
            volume=volume
        ))
        return response

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Bacterie</title></head>
<body>
    <h1>Bacterie</h1>
    <p>Etat actuel : <b>{{ state }}</b></p>
    <p>Volume : <b>{{ volume }}</b> m³</p>
    <h2>Changer d'etat :</h2>
    {% for s in available_states %}
    <form method="POST" action="/transition">
        <input type="hidden" name="new_state" value="{{ s }}">
        <button type="submit">→ {{ s }}</button>
    </form>
    {% endfor %}
    {% if not available_states %}
    <p>Aucune transition possible (impasse)</p>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    response = call_state(bacterie['state'], bacterie['volume'])
    bacterie['volume'] = response.volume
    return render_template_string(HTML,
        state=bacterie['state'],
        volume=round(bacterie['volume'], 4),
        available_states=response.available_states
    )

@app.route('/transition', methods=['POST'])
def transition():
    new_state = request.form.get('new_state')
    if new_state in STATE_PORTS:
        bacterie['state'] = new_state
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
