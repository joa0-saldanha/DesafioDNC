from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator

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
        dag_id=f'cleaunup',
        description=f'Cleanup the HISTORICAL DATA on the DATABASE',
        tags=['cleaunup', 'forecast', 'traffic'],
        start_date=datetime(2024, 1, 13),
        schedule_interval='59 21 * * *', 
        default_args=args,
        catchup=False,
        dagrun_timeout=timedelta(minutes=60),
        max_active_runs=1,
        template_searchpath=["/home/airflow/gcs/data"],
        is_paused_upon_creation=True
) as dag:

    clean_historical_traffic = BigQueryExecuteQueryOperator(
        task_id='clean_historical_traffic',
        sql="sql/clean_historical_traffic.sql",
        use_legacy_sql=False
    )

    clean_historical_forecast = BigQueryExecuteQueryOperator(
        task_id='clean_historical_forecast',
        sql="sql/clean_historical_forecast.sql",
        use_legacy_sql=False
    )

    clean_historical_traffic >> clean_historical_forecast
