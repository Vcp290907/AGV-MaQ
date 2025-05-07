from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import serial
import threading
import time
try:
    import RPi.GPIO as GPIO
except ImportError:
    # Mock GPIO for non-Raspberry Pi environments
    class MockGPIO:
        BCM = HIGH = LOW = OUT = None
        @staticmethod
        def setmode(mode): pass
        @staticmethod
        def setup(pin, mode): pass
        @staticmethod
        def output(pin, state): pass
        @staticmethod
        def cleanup(): pass
    GPIO = MockGPIO()

app = Flask(__name__)
CORS(app)

# Configura o pino GPIO para o buzzer
BUZZER_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# Configura o banco de dados SQLite
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS temperatures
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, value REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Função para ler dados seriais do ESP32
def read_serial():
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        time.sleep(2)
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                try:
                    temp = float(line)
                    conn = sqlite3.connect('data.db')
                    c = conn.cursor()
                    c.execute('INSERT INTO temperatures (value) VALUES (?)', (temp,))
                    conn.commit()
                    conn.close()
                except ValueError:
                    print(f"Dado inválido recebido: {line}")
            time.sleep(0.1)
    except Exception as e:
        print(f"Erro na comunicação serial: {e}")

# Rota para obter temperaturas
@app.route('/api/temperatures', methods=['GET'])
def get_temperatures():
    try:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('SELECT * FROM temperatures ORDER BY timestamp DESC LIMIT 100')
        temperatures = [{'id': row[0], 'value': row[1], 'timestamp': row[2]} for row in c.fetchall()]
        conn.close()
        return jsonify(temperatures), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao consultar temperaturas: {str(e)}'}), 500

# Rota para acionar o buzzer
@app.route('/api/buzzer', methods=['POST'])
def activate_buzzer():
    try:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        return jsonify({'message': 'Buzzer acionado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao acionar o buzzer: {str(e)}'}), 500

if __name__ == '__main__':
    init_db()
    try:
        serial_thread = threading.Thread(target=read_serial, daemon=True)
        serial_thread.start()
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        GPIO.cleanup()