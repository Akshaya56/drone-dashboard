from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
import sqlite3

app = Flask(__name__)
app.secret_key = 'stark_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# User model
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        return User(*row)
    return None

# ---------------- Routes ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row and check_password_hash(row[2], password):
            user = User(*row)
            login_user(user)
            return redirect(url_for('index'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/telemetry')
@login_required
def telemetry():
    return jsonify({
        'battery_voltage': round(random.uniform(10.0, 12.6), 2),
        'imu': {
            'roll': round(random.uniform(-180, 180), 2),
            'pitch': round(random.uniform(-90, 90), 2),
            'yaw': round(random.uniform(-180, 180), 2)
        },
        'temperature': round(random.uniform(20.0, 40.0), 2),
        'altitude': round(random.uniform(0, 100), 2),
        'gps': f"{round(random.uniform(12.9, 13.1), 6)}, {round(random.uniform(77.5, 77.7), 6)}",
        'connection_health': random.choice(["Excellent", "Good", "Poor", "No Signal"])
    })

# ---------------- Register New Users ----------------
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = generate_password_hash(request.form['password'])
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return redirect(url_for('login'))
    except:
        return "User already exists"

if __name__ == '__main__':
    app.run(debug=True)
