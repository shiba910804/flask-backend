
from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# 設置資料庫連接信息，從環境變數或直接在這裡設置
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://flutter_number_user:4LWRRPFkLPyLtJ1PzTRLkfGxS4CpDNNg@dpg-crksia3v2p9s73e70tfg-a.singapore-postgres.render.com/flutter_number')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# 正文頁面
@app.route('/')
def home():
    return "Hello, this is the home page of your Flask application."

# 註冊 API
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO merchants (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Registration successful"}), 201

# 登入 API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM merchants WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)