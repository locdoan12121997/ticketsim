## Setup Airflow VM

![airflow](../images/airflow.jpg)

We will setup airflow on docker in a dedicated compute instance. dbt is setup inside airflow.

- Access SSH to airflow vm instance
- Clone git repo and cd to kafka folder

  ```bash
  git clone https://github.com/locdoan12121997/ticketsim.git
  ```

- Install docker & docker-compose

  ```bash
  bash ~/ticketsim/scripts/vm_setup.sh && exec newgrp docker
  ```

- Move the service account json file from local to the VM machine in `~/.google/credentials/` directory.  Make sure it is named as `key.json`  else the dags will fail!

- Set the evironment variables

  - GCP Project ID

  - Cloud Storage Bucket Name

  - BigQuery Dataset

    ```bash
    export GCP_PROJECT_ID=project-id
    export GCP_GCS_BUCKET=bucket-name
    export BIGQUERY_DATASET=bigquery_dataset_name
    ```

    **Note**: You will have to setup these env vars every time you create a new shell session.

- Set permission for dbt folder so that docker can access and edit the logs file

    ```bash
    sudo chmod -R 777 dbt_transform
    ```


- Start airflow

    ```bash
    docker-compose up airflow-init && docker-compose up
    ```

- To stop airflow

    ```bash
    docker-compose down -v
    ```
