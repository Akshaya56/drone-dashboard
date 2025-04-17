from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    telemetry = {
        "battery_voltage": round(random.uniform(10, 12), 2),
        "roll": round(random.uniform(-180, 180), 2),
        "pitch": round(random.uniform(-90, 90), 2),
        "yaw": round(random.uniform(-180, 180), 2),
        "temperature": round(random.uniform(20, 40), 2),
        "altitude": round(random.uniform(0, 1000), 2),
        "latitude": round(random.uniform(-90, 90), 6),
        "longitude": round(random.uniform(-180, 180), 6),
        "connection_health": random.choice(["Excellent", "Good", "Poor", "No Signal"])
    }
    return jsonify(telemetry)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
