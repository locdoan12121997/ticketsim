export GCP_PROJECT_ID=elite-bird-367213
export GCP_GCS_BUCKET=ticketsim
export BIGQUERY_DATASET=bq_ticketsim
export AIRFLOW_UID=50000

sudo chmod -R 777 dbt_transform
docker-compose up airflow-init
docker-compose up
docker-compose down -v