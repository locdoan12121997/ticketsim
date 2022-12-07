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

add firewall rules:

export KAFKA_ADDRESS=10.148.0.2
export GCP_GCS_BUCKET=ticketsim

One experience to run commands are check spark and its dependency version. Run pyspark command can check spark version

dataproc
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3 stream_events.py

local
./spark-submit --jars ./gcs-connector-hadoop3-2.1.9-shaded.jar --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 --conf spark.hadoop.fs.gs.impl=com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem --conf spark.hadoop.google.cloud.auth.service.account.enable=true --conf spark.hadoop.google.cloud.auth.service.account.json.keyfile=/home/locdoan12121997/nhacmoi/spark/key.json ~/nhacmoi/spark/stream_events.py

Give service account permission
storage permission
gsutil iam ch serviceAccount:locdoan12121997@elite-bird-367213.iam.gserviceaccount.com:admin gs://ticketsim
gcloud projects add-iam-policy-binding elite-bird-367213 --member=serviceAccount:locdoan12121997@elite-bird-367213.iam.gserviceaccount.com --role=roles/bigquery.admin
ref: https://stackoverflow.com/questions/42564112/adding-roles-to-service-accounts-on-google-cloud-platform-using-rest-api