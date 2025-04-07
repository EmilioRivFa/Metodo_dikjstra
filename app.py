from flask import Flask, request, jsonify, render_template
import heapq

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dijkstra', methods=['POST'])
def dijkstra():
    data = request.get_json()
    nodes = data['nodes']
    edges = data['edges']
    start = data['start']
    end = data['end']

    # Construcción del grafo
    graph = {node['id']: {} for node in nodes}
    for edge in edges:
        graph[edge['from']][edge['to']] = int(edge['label'])

    # Dijkstra
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    prev = {node: None for node in graph}
    queue = [(0, start)]

    while queue:
        dist, current = heapq.heappop(queue)

        if current == end:
            break

        for neighbor, weight in graph[current].items():
            alt = dist + weight
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                prev[neighbor] = current
                heapq.heappush(queue, (alt, neighbor))

    # Reconstruir camino
    path = []
    node = end
    while node:
        path.insert(0, node)
        node = prev[node]

    return jsonify({'distance': distances[end], 'path': path})

if __name__ == '__main__':
    app.run(debug=True)
