import json
import time
from kafka import KafkaProducer
import os
import random
from datetime import datetime

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'ships_topic')
KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'kafka:9092')
FETCH_INTERVAL = 10  # 10s pour test, passe à 60s pour la prod

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_mock_ships(nb=3):
    ships = []
    for i in range(nb):
        ships.append({
            "mmsi":  f"12345678{i}",
            "ship_name": f"SHIP_{i}",
            "lat": round(random.uniform(-90, 90), 6),
            "lon": round(random.uniform(-180, 180), 6),
            "speed": round(random.uniform(0, 25), 2),
            "course": round(random.uniform(0, 360), 1),
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        })
    return ships

def fetch_ships():
    # --- MOCK ---
    return generate_mock_ships()

if __name__ == "__main__":
    while True:
        ships_data = fetch_ships()
        producer.send(KAFKA_TOPIC, ships_data)
        producer.flush()
        print(f"[MOCK FETCH] {len(ships_data)} ships envoyés à Kafka !")
        time.sleep(FETCH_INTERVAL)
