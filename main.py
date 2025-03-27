from flask import Flask, request, jsonify
import jwt
import datetime
import sqlite3
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# --- Banco de Dados ---
def connect_db():
    return sqlite3.connect('data.db')

def create_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value TEXT NOT NULL
            )"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )"""
        )
        conn.commit()
create_table()

# --- Autenticação JWT ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token ausente'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'error': 'Token inválido'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    username = auth.get('username')
    password = auth.get('password')
    
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
    
    if user:
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return jsonify({'error': 'Credenciais inválidas'}), 401

# --- Rotas Protegidas ---
@app.route('/data', methods=['POST', 'GET'])
@token_required
def data():
    if request.method == "POST":
        value = request.json.get('data')
        if not value:
            return jsonify({"error": "No value provided"}), 400
        
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO data (value) VALUES (?)', (value,))
            conn.commit()
        return jsonify({"message": "Value added successfully"}), 201

    elif request.method == "GET":
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM data')
            rows = cursor.fetchall()
        return jsonify([{"id": row[0], "data": row[1]} for row in rows]), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
