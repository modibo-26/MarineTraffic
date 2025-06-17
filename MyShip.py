import requests
import time
from kafka import KafkaProducer
import json
import os

os.getenv("API_URL")

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_vessels():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        return None

while True:
    data = fetch_vessels()
    if data:
        producer.send('vessel_positions', data)
        print(f"{len(data)} navires envoyés à Kafka")
    time.sleep(60)  # Toutes les minutes