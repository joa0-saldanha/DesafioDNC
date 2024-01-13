from datetime import datetime, timedelta

from airflow.models import DAG
from operators.gcp_functions import CallGoogleCloudFunctionsOperator

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
        function_name='traffic',
        response_type='text'
    )

    call_function