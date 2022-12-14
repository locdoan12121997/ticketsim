## Terraform Infra Setup

- Clone git repo and cd to terraform directory

  ```bash
  git clone https://github.com/locdoan12121997/ticketsim.git && cd terraform
  ```

- Init terraform

  ```bash
  terraform init
  ```

- View the Terraform plan

  You will be asked to enter the name of the GCS bucket you want to create, your GCP Project ID, and non-quoted path to service account json. Use the same values throughout the project. 

  ```bash
  terraform plan
  ```

  - Apply the infra. **Note** - Billing will start as soon as the apply is complete.

  ```bash
  terraform apply
  ```

  - Once you are done with the project. Teardown the infra using-

  ```bash
  terraform destroy
  ```