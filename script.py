import requests
import time
from kafka import KafkaProducer
import os

# Configuration
API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')
KAFKA_BROKER = "kafka-broker:9092"
TOPIC = "ais_data"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_ship_data():
    params = {
        "vessel_id": 0,  # 0 = tous les navires
        "timespan": 60,   # 60 secondes
        "protocol": "json",
        "api_key": API_KEY
    }
    response = requests.get(API_URL, params=params)
    return response.json().get('data', [])

while True:
    ships = fetch_ship_data()
    for ship in ships:
        producer.send(TOPIC, ship)
    time.sleep(60)  # Toutes les minutes