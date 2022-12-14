Give service account permission
storage permission
gsutil iam ch serviceAccount:locdoan12121997@elite-bird-367213.iam.gserviceaccount.com:admin gs://ticketsim
gcloud projects add-iam-policy-binding elite-bird-367213 --member=serviceAccount:locdoan12121997@elite-bird-367213.iam.gserviceaccount.com --role=roles/bigquery.admin
ref: https://stackoverflow.com/questions/42564112/adding-roles-to-service-accounts-on-google-cloud-platform-using-rest-api

Airflow
export GCP_PROJECT_ID=elite-bird-367213
export GCP_GCS_BUCKET=ticketsim
export BIGQUERY_DATASET=bq_ticketsim
export AIRFLOW_UID=50000