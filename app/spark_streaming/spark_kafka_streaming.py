from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, DoubleType

KAFKA_SERVER = 'kafka:9092'
KAFKA_TOPIC = 'ships_topic'

ship_schema = StructType([
    StructField("mmsi", StringType(), True),
    StructField("ship_name", StringType(), True),
    StructField("lat", DoubleType(), True),
    StructField("lon", DoubleType(), True),
    StructField("speed", DoubleType(), True),
    StructField("course", DoubleType(), True),
    StructField("timestamp", StringType(), True),
])

spark = SparkSession.builder \
    .appName("ShipKafkaStreaming") \
    .getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

df = df.selectExpr("CAST(value AS STRING) as json_str")
ships_df = df.withColumn("ships", from_json(col("json_str"), ArrayType(ship_schema)))
ships_df = ships_df.withColumn("ship", explode(col("ships")))

# Filtre sur les navires lents (<3 nœuds)
slow_ships_df = ships_df.select("ship.*").where(col("ship.speed") < 3)

# Export vers console OU CSV
query = slow_ships_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

# Pour exporter vers CSV, décommente la partie ci-dessous

# query = slow_ships_df.writeStream \
#     .outputMode("append") \
#     .format("csv") \
#     .option("path", "/app/spark_streaming/export_csv") \
#     .option("checkpointLocation", "/app/spark_streaming/checkpoints") \
#     .start()

query.awaitTermination()
