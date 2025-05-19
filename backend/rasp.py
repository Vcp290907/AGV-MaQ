import requests
import time

API_URL = "http://<ip_do_servidor>:5000/api/temperatures"

while True:
    temperatura = 25.0  # Leia do sensor real aqui
    try:
        requests.post(API_URL, json={'value': temperatura})
    except Exception as e:
        print(f"Erro ao enviar temperatura: {e}")
    time.sleep(10)