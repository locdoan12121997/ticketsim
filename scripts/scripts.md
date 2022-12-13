Give service account permission
storage permission
gsutil iam ch serviceAccount:locdoan12121997@elite-bird-367213.iam.gserviceaccount.com:admin gs://ticketsim
gcloud projects add-iam-policy-binding elite-bird-367213 --member=serviceAccount:locdoan12121997@elite-bird-367213.iam.gserviceaccount.com --role=roles/bigquery.admin
ref: https://stackoverflow.com/questions/42564112/adding-roles-to-service-accounts-on-google-cloud-platform-using-rest-api
