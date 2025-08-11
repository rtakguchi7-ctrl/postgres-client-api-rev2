from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres'),
        database=os.environ.get('DB_NAME', 'sensor_db'),
        user=os.environ.get('DB_USER', 'user'),
        password=os.environ.get('DB_PASSWORD', 'password')
    )

@app.route('/data', methods=['POST'])
def insert_or_update_data():
    data = request.get_json()
    id = data.get('id')
    value = data.get('value')
    timestamp = data.get('timestamp')

    if not all([id, value, timestamp]):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    query = (
        "INSERT INTO sensor_data (id, value, timestamp) "
        "VALUES (%s, %s, %s) "
        "ON CONFLICT (id) DO UPDATE SET value = EXCLUDED.value, timestamp = EXCLUDED.timestamp;"
    )
    cur.execute(query, (id, value, timestamp))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Data inserted or updated successfully'}), 200

@app.route('/data/<id>', methods=['DELETE'])
def delete_data(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM sensor_data WHERE id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': f'Data with id {id} deleted successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
