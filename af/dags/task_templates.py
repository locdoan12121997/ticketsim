from airflow.providers.google.cloud.operators.bigquery import (BigQueryCreateExternalTableOperator, 
                                                               BigQueryCreateEmptyTableOperator, 
                                                               BigQueryInsertJobOperator,
                                                               BigQueryDeleteTableOperator)


def create_external_table(event,
                          gcp_project_id, 
                          bigquery_dataset, 
                          external_table_name, 
                          gcp_gcs_bucket, 
                          events_path):
    task = BigQueryCreateExternalTableOperator(
        task_id = f'{event}_create_external_table',
        table_resource = {
            'tableReference': {
                'projectId': gcp_project_id,
                'datasetId': bigquery_dataset,
                'tableId': f'{external_table_name}',
            },
            'externalDataConfiguration': {
                'sourceFormat': 'PARQUET',
                'sourceUris': [f'gs://{gcp_gcs_bucket}/{events_path}/*.parquet'],
            },
        }
    )

    return task
