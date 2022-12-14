## GCP

### Initial Setup

Checkout this [video](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=13)

1. Create an account with your Google email ID 
2. Setup your first [project](https://console.cloud.google.com/) if you haven't already
    * eg. "Ticketsim", and note down the "Project ID" (we'll use this later when deploying infra)
3. Setup [service account & authentication](https://console.cloud.google.com/iam-admin/serviceaccounts) for this project
    * Grant following role:
        * Compute Security Admin
        * BigQuery Admin
        * Editor
        * Storage Admin
        * Storage Object Admin
        * Dataproc Administrator
        * Compute Instance Admin (beta)
    * Download service-account-keys (`.json`) for auth. (Please do not share this key file publicly. Keep it secure!)
    * Rename the `.json` key file to `key.json`
    * If terraform output any error regarding lack of permission, you can activate cloud shell and use the following command to add role to your service account
   ```shell
   gcloud projects add-iam-policy-binding PROJECT-NAME --member=serviceAccount:your-serviceaccount --role=roles/the.role.you.lack
   ```
4. Download [SDK](https://cloud.google.com/sdk/docs/quickstart) for local setup
5. Set environment variable to point to your downloaded GCP keys:
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/google_credentials/key.json>"
   
   # Refresh token/session, and verify authentication
   gcloud auth application-default login
   ```
   
### Setup for Access

1. [IAM Roles](https://cloud.google.com/storage/docs/access-control/iam-roles) for Service account:
   * Go to the *IAM* section of *IAM & Admin* https://console.cloud.google.com/iam-admin/iam
   * Click the *Edit principal* icon for your service account.
   * Add these roles in addition to *Viewer* : **Storage Admin** + **Storage Object Admin** + **BigQuery Admin**
   
2. Enable these APIs for your project:
   * https://console.cloud.google.com/apis/library/iam.googleapis.com
   * https://console.cloud.google.com/marketplace/product/google/iamcredentials.googleapis.com
   * https://console.cloud.google.com/dataproc/clusters
   * **Note:** You might have to enable a few APIs here and there like DataProc etc.