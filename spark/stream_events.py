import os
from stream_functions import create_or_get_spark_session, create_kafka_read_stream, process_stream, create_file_write_stream
from schema import schema

# Kafka Topics
SCANNER_LINE_EVENTS_TOPIC = "wait_in_scanner_line"
SELLER_LINE_EVENTS_TOPIC = "wait_in_seller_line"

KAFKA_PORT = "9092"

KAFKA_ADDRESS = os.getenv("KAFKA_ADDRESS", 'localhost')
GCP_GCS_BUCKET = os.getenv("GCP_GCS_BUCKET", 'ticketsim')
GCS_STORAGE_PATH = f'gs://{GCP_GCS_BUCKET}'

# initialize a spark session
spark = create_or_get_spark_session('Ticket Stream')
spark.streams.resetTerminated()
# listen events stream
scanner_line_events = create_kafka_read_stream(
    spark, KAFKA_ADDRESS, KAFKA_PORT, SCANNER_LINE_EVENTS_TOPIC)
scanner_line_events = process_stream(
    scanner_line_events, schema[SCANNER_LINE_EVENTS_TOPIC], SCANNER_LINE_EVENTS_TOPIC)

# page view stream
seller_line_events = create_kafka_read_stream(
    spark, KAFKA_ADDRESS, KAFKA_PORT, SELLER_LINE_EVENTS_TOPIC)
seller_line_events = process_stream(
    seller_line_events, schema[SELLER_LINE_EVENTS_TOPIC], SELLER_LINE_EVENTS_TOPIC)

# write a file to storage every 2 minutes in parquet format
scanner_line_events_writer = create_file_write_stream(scanner_line_events,
                                                f"{GCS_STORAGE_PATH}/{SCANNER_LINE_EVENTS_TOPIC}",
                                                f"{GCS_STORAGE_PATH}/checkpoint/{SCANNER_LINE_EVENTS_TOPIC}"
                                                )

scanner_line_events_writer = create_file_write_stream(seller_line_events,
                                                   f"{GCS_STORAGE_PATH}/{SELLER_LINE_EVENTS_TOPIC}",
                                                   f"{GCS_STORAGE_PATH}/checkpoint/{SELLER_LINE_EVENTS_TOPIC}"
                                                   )

scanner_line_events_writer.start()
scanner_line_events_writer.start()

spark.streams.awaitAnyTermination()
