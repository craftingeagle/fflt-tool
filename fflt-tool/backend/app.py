from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Database connection
DATABASE = 'backend/database.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/loot', methods=['GET'])
def get_loot():
    # Retrieve loot data from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM loot')
    loot_data = cursor.fetchall()
    conn.close()
    return jsonify({'loot': [dict(row) for row in loot_data]})

@app.route('/api/loot', methods=['POST'])
def add_loot():
    # Add new loot data to the database
    new_loot = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO loot (name, type, coordinates) VALUES (?, ?, ?)', 
                   (new_loot['name'], new_loot['type'], new_loot['coordinates']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Loot added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
