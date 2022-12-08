from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, month, hour, dayofmonth, col, year, udf


def create_or_get_spark_session(app_name, master="yarn"):
    spark = (SparkSession
             .builder
             .appName(app_name)
            #  .master(master="spark://de-zoomcamp.asia-southeast1-b.c.elite-bird-367213.internal:4040")
            #  .master(master=master)
             .getOrCreate())
    return spark


def create_kafka_read_stream(spark, kafka_address, kafka_port, topic, starting_offset="earliest"):
    read_stream = (spark
                   .readStream
                   .format("kafka")
                   .option("kafka.bootstrap.servers", f"{kafka_address}:{kafka_port}")
                   .option("failOnDataLoss", False)
                   .option("startingOffsets", starting_offset)
                   .option("subscribe", topic)
                   .load())
    return read_stream


def process_stream(stream, stream_schema, topic):
    stream = (stream
              .selectExpr("CAST(value AS STRING)")
              .select(
                  from_json(col("value"), stream_schema).alias(
                      "data")
              )
              .select("data.*")
              )
    return stream


def create_file_write_stream(stream, storage_path, checkpoint_path, trigger="120 seconds", output_mode="append", file_format="parquet"):
    write_stream = (stream
                    .writeStream
                    .format(file_format)
                    .option("path", storage_path)
                    .option("checkpointLocation", checkpoint_path)
                    .trigger(processingTime=trigger)
                    .outputMode(output_mode))
    return write_stream
