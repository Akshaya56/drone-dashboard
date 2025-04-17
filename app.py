from flask import Flask, render_template, jsonify
import random
import time

app = Flask(__name__)

# Simulate starting drone coordinates and some obstacles
drone_position = {'x': 50, 'y': 50}
obstacles = [{'x': random.randint(0, 100), 'y': random.randint(0, 100)} for _ in range(5)]

def move_drone():
    # Simulate smooth movement in 2D space
    drone_position['x'] += random.choice([-1, 0, 1])
    drone_position['y'] += random.choice([-1, 0, 1])
    drone_position['x'] = max(0, min(100, drone_position['x']))
    drone_position['y'] = max(0, min(100, drone_position['y']))

    return drone_position

def calculate_status():
    closest_distance = 999
    for obs in obstacles:
        dx = drone_position['x'] - obs['x']
        dy = drone_position['y'] - obs['y']
        distance = (dx**2 + dy**2)**0.5
        if distance < closest_distance:
            closest_distance = distance

    if closest_distance < 10:
        return 'Danger'
    elif closest_distance < 20:
        return 'Caution'
    else:
        return 'Safe'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/telemetry')
def telemetry():
    move_drone()
    status = calculate_status()
    return jsonify({
        'drone': drone_position,
        'obstacles': obstacles,
        'status': status
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
