import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

from task_templates import create_external_table

EVENTS = ['wait_in_scanner_line', 'wait_in_seller_line']
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCP_GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
BIGQUERY_DATASET = os.environ.get('BIGQUERY_DATASET', 'bq_ticketsim')
EXECUTION_MONTH = '{{ logical_date.strftime("%-m") }}'
EXECUTION_DAY = '{{ logical_date.strftime("%-d") }}'
EXECUTION_HOUR = '{{ logical_date.strftime("%-H") }}'
EXECUTION_DATETIME_STR = '{{ logical_date.strftime("%m%d") }}'

TABLE_MAP = { f"{event.upper()}_TABLE" : event for event in EVENTS}

MACRO_VARS = {"GCP_PROJECT_ID":GCP_PROJECT_ID, 
              "BIGQUERY_DATASET": BIGQUERY_DATASET, 
              "EXECUTION_DATETIME_STR": EXECUTION_DATETIME_STR
              }

MACRO_VARS.update(TABLE_MAP)

default_args = {
    'owner' : 'airflow'
}
with DAG(
    dag_id = f'ticketsim_dag',
    default_args = default_args,
    description = f'Hourly data pipeline to generate dims and facts for ticketsim',
    schedule_interval="5 * * * *", #At the 5th minute of every hour
    start_date=datetime(2022,12,12,18),
    catchup=False,
    max_active_runs=1,
    user_defined_macros=MACRO_VARS,
    tags=['ticketsim']
) as dag:

    execute_dbt_task = BashOperator(
        task_id = 'dbt_ticketsim_run',
        bash_command = 'cd /dbt && dbt run --profiles-dir . --target prod'
    )

    for event in EVENTS:
        
        staging_table_name = event
        external_table_name = f'{staging_table_name}_{EXECUTION_DATETIME_STR}'
        events_data_path = f'{staging_table_name}'

        create_external_table_task = create_external_table(event,
                                                           GCP_PROJECT_ID, 
                                                           BIGQUERY_DATASET, 
                                                           external_table_name, 
                                                           GCP_GCS_BUCKET, 
                                                           events_data_path)        
        create_external_table_task

    execute_dbt_task
