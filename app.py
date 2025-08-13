from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL connection settings from environment variables
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO sensor_data (id, value) VALUES (%s, %s)", (data['id'], data['value']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "uploaded"}), 201

@app.route('/read', methods=['GET'])
def read():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensor_data")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM sensor_data WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "deleted"}), 200

@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE sensor_data SET value = %s WHERE id = %s", (data['value'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "updated"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
