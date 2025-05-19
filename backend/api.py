from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# backend/api.py
@app.route('/api/comando', methods=['POST'])
def comando():
    data = request.get_json()
    item1 = data.get('item1', False)
    item2 = data.get('item2', False)
    print(f"Comando recebido do frontend: item1={item1}, item2={item2}", flush=True)
    return jsonify({'message': f'Comando recebido: item1={item1}, item2={item2}'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)