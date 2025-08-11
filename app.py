from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Database connection parameters from environment variables
DB_HOST = os.getenv('DB_HOST', 'local-postgres')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'mydb')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'adminpass')

def get_connection():
    import psycopg2
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route('/data', methods=['POST'])
def insert_or_update_data():
    try:
        data = request.get_json(force=True)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id TEXT PRIMARY KEY,
                value TEXT,
                timestamp TIMESTAMP
            )
        """)
        cur.execute("""
            INSERT INTO sensor_data (id, value, timestamp)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                value = EXCLUDED.value,
                timestamp = EXCLUDED.timestamp
        """, (data['id'], data['value'], data['timestamp']))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Data inserted or updated"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data/<id>', methods=['DELETE'])
def delete_data(id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM sensor_data WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": f"Data with id '{id}' deleted"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data', methods=['GET'])
def get_all_data():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sensor_data")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
