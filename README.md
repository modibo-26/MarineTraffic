# MarineTraffic - Flux maritime temps réel

## 🛠️ Prérequis

- Docker & Docker Compose
- Python 3.x pour les tests locaux

---

## 🚀 Lancer toute la stack

```bash (à la racine MarineTraffic)

docker-compose up -d --build

//////////////////

📤 Publier des données navires (mock)
Dans un terminal :

docker-compose exec python-app bash
python fetcher/fetch_live_data.py

Modifiez fetch_live_data.py pour utiliser l’API réelle dès que dispo.

//////////////

👀 Consommer les messages Kafka (test ou UI)

docker-compose exec python-app bash
python kafka_producer/consumer_test.py

Ce script affiche en temps réel tout message publié sur le topic ships_topic.

//////////////

⚡ Lancer Spark Streaming (analyse des flux Kafka)

docker-compose exec spark bash
export HOME=/tmp
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.2 /app/spark_streaming/spark_kafka_streaming.py

Ce script affiche à la console les navires “lents” (vitesse < 3) reçus via Kafka.

//////////////

Brancher une vraie API navires

Dans fetch_live_data.py, modifiez la fonction fetch_ships() 

Placez votre clé dans .env ou en variable d'env Docker.