Install spark
wget https://dlcdn.apache.org/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz

Unpack
tar xzfv spark-3.3.1-bin-hadoop3.tgz

Remove the archive
rm spark-3.3.1-bin-hadoop3.tgz

export SPARK_HOME="${HOME}/spark-3.3.1-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
export GCP_GCS_BUCKET=ticketsim

spark://de-zoomcamp.asia-southeast1-b.c.elite-bird-367213.internal:4040