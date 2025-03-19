from flask import Flask, request, jsonify, send_from_directory
from collections import deque
import os

app = Flask(__name__)

def bfs(start, goal):
    queue = deque([(start, [])])
    visited = set()

    while queue:
        state, path = queue.popleft()
        if state == goal:
            return path + [state]
        if state in visited:
            continue
        visited.add(state)
        for next_state in get_neighbors(state):
            if next_state not in visited:
                queue.append((next_state, path + [state]))

    return []

def dfs(start, goal):
    stack = [(start, [])]
    visited = set()

    while stack:
        state, path = stack.pop()
        if state == goal:
            return path + [state]
        if state in visited:
            continue
        visited.add(state)
        for next_state in get_neighbors(state):
            if next_state not in visited:
                stack.append((next_state, path + [state]))

    return []

def dfs_recursive(state, goal, path=None, visited=None):
    if path is None:
        path = []
    if visited is None:
        visited = set()

    if state == goal:
        return path + [state]
    if state in visited:
        return []

    visited.add(state)
    for next_state in get_neighbors(state):
        result = dfs_recursive(next_state, goal, path + [state], visited)
        if result:
            return result

    return []

def get_neighbors(state):
    neighbors = []
    for i in range(len(state) - 1):
        new_state = list(state)
        new_state[i], new_state[i + 1] = new_state[i + 1], new_state[i]
        neighbors.append(tuple(new_state))
    return neighbors

@app.route('/')
def home():
    return send_from_directory(os.path.dirname(__file__), "index.html")

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()

        if not data or 'start' not in data or 'goal' not in data or 'method' not in data:
            return jsonify({'error': 'Faltan parámetros'}), 400

        start = tuple(data['start'])
        goal = tuple(data['goal'])
        method = data['method'].upper()

        if method == 'BFS':
            solution = bfs(start, goal)
        elif method == 'DFS':
            solution = dfs(start, goal)
        elif method == 'DFS_REC':
            solution = dfs_recursive(start, goal)
        else:
            return jsonify({'error': 'Método no válido'}), 400

        return jsonify({'solution': solution})

    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)