from datetime import datetime, timedelta

from airflow.models import DAG
from operators.gcp_functions import CallGoogleCloudFunctionsOperator
from airflow.providers.google.operators.transfers.gcs_to_bigquery import GCSToBigQueryOperator


schema = [
        {'name': 'id',              'type': 'INTEGER'},				
        {'name': 'city',            'type': 'INTEGER'},				
        {'name': 'date',            'type': 'DATE'},				
        {'name': 'hour',            'type': 'TIME'},				
        {'name': 'temperature',     'type': 'FLOAT64'},				
        {'name': 'humidity',        'type': 'FLOAT64'},				
        {'name': 'precipitation',   'type': 'FLOAT64'}
    ]

args = {
    'owner': 'data_lake',
    'depends_on_past': False,
    'wait_for_downstream': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=30),
    'execution_timeout': timedelta(minutes=60),
}

with DAG(
        dag_id=f'forecast',
        description=f'Get FORECAST informations to the DATABASE',
        tags=['forecast'],
        start_date=datetime(2024, 1, 13),
        schedule_interval='10 3 * * *', 
        default_args=args,
        catchup=False,
        dagrun_timeout=timedelta(minutes=60),
        max_active_runs=1,
        template_searchpath=["/home/airflow/gcs/data"],
        is_paused_upon_creation=True
) as dag:

    call_function = CallGoogleCloudFunctionsOperator(
        task_id='call_function',
        function_name='api-to-gcs',
        function_params={
            "task": "forecast",
            "datetime": "{{ data_interval_end | ts_nodash }}"
        },
        response_type='text'
    )

    json_to_table = GCSToBigQueryOperator(
        task_id='json_to_table',
        bucket="dnc-forecast-traffic-data",
        source_objects="{{ ti.xcom_pull(task_ids='call_function') }}",
        destination_project_dataset_table="estudos-410923.DNC.forecast",
        source_format='NEWLINE_DELIMITED_JSON',
        schema_fields=schema,
        write_disposition='WRITE_TRUNCATE',
        create_disposition='CREATE_IF_NEEDED', 
        ignore_unknown_values=True
    )

    call_function >> json_to_table
