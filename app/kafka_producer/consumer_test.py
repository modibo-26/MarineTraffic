from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'ships_topic',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda x: x.decode('utf-8'),
    auto_offset_reset='earliest'
)

for msg in consumer:
    print(msg.value)
