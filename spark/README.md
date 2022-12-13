## Setup Spark Cluster

![spark](../images/spark.jpg)

- For creating Spark cluster, you can follow instruction in this [video](https://www.youtube.com/watch?v=osAiAYahvh8&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=62)

- Access to dataproc cluster

- Clone git repo

  ```bash
  git clone https://github.com/locdoan12121997/ticketsim.git &&  cd ticketsim/spark
  ```

- Set the evironment variables -

  - External IP of the Kafka VM so that spark can connect to it

  - Name of your GCS bucket. (What you gave during the terraform setup)

    ```bash
    export KAFKA_ADDRESS=IP.ADD.RE.SS
    export GCP_GCS_BUCKET=bucket-name
    ```

     **Note**: You will have to setup these env vars every time you create a new shell session. Or if you stop/start your cluster

- Start reading messages

  ```bash
  spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3 stream_events.py
  ```

     **Note**: One experience to run commands are check spark and its dependency version for the 0-10_2.12:3.1.3 part or the command will exit with error. Run pyspark command can check spark version

- If all went right, you should see new `parquet` files in your bucket! That is Spark writing a file every two minutes for each topic.

If you want a local setup for standalone spark app

## Setup Local Single Machine Spark

- Download java, spark and setup environment variables

  ```bash
  bash ~/scripts/local_spark_setup.sh
  ```

- Export bucket name to environment variable

  ```bash
  export GCP_GCS_BUCKET=yourbucket
  ```

- Add firewall rules on GCP for port `9092` on kafka instance

- Run local spark job

  ```bash
  ./spark-submit --jars ./gcs-connector-hadoop3-2.1.9-shaded.jar --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 --conf spark.hadoop.fs.gs.impl=com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem --conf spark.hadoop.google.cloud.auth.service.account.enable=true --conf spark.hadoop.google.cloud.auth.service.account.json.keyfile=/home/locdoan12121997/nhacmoi/spark/key.json ~/nhacmoi/spark/stream_events.py
  ```
