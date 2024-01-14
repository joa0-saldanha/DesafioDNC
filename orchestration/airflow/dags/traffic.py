from datetime import datetime, timedelta

from airflow.models import DAG
from operators.gcp_functions import CallGoogleCloudFunctionsOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator



schema = [				
        {'name': 'route',                           'type': 'INTEGER'},				
        {'name': 'lengthInMeters',              'type': 'INTEGER'},				
        {'name': 'travelTimeInSeconds',          'type': 'INTEGER'},				
        {'name': 'trafficDelayInSeconds',        'type': 'INTEGER'},				
        {'name': 'trafficLengthInMeters',      'type': 'INTEGER'},				
        {'name': 'departureTime',                  'type': 'INTEGER'},				
        {'name': 'arrivalTime',                        'type': 'TIMESTAMP'},
        {'name': 'id',                              'type': 'INTEGER'}
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
        dag_id=f'traffic',
        description=f'Get TRAFFIC informations to the DATABASE',
        tags=['traffic'],
        start_date=datetime(2024, 1, 13),
        schedule_interval='0 * * * *', 
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
            "task": "traffic",
            "datetime": "{{ data_interval_end | ts_nodash }}"
        },
        response_type='text'
    )

    json_to_table = GCSToBigQueryOperator(
        task_id='json_to_table',
        bucket="dnc-forecast-traffic-data",
        source_objects="{{ ti.xcom_pull(task_ids='call_function') }}",
        destination_project_dataset_table="estudos-410923.DNC.traffic",
        source_format='NEWLINE_DELIMITED_JSON',
        schema_fields=schema,
        write_disposition='WRITE_TRUNCATE',
        create_disposition='CREATE_IF_NEEDED', 
        ignore_unknown_values=True
    )

    call_function >> json_to_table
