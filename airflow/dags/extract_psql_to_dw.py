import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta

default_args = {
    'owner': 'grab_zzang@gmail.com',
    'start_date': datetime(2023, 1, 18),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'extract_psql_to_dw',
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
    catchup=False,
)

def migrate_data(ds, **kwargs):
    src_hook = PostgresHook(postgres_conn_id='source_db_connection')
    src_table = 'public.order_items'

    df = src_hook.get_pandas_df(f'SELECT * FROM {src_table}')

    dst_hook = PostgresHook(postgres_conn_id='dst_db_connection')
    dst_engine = dst_hook.get_sqlalchemy_engine()
    dst_table = 'order_items'
    dst_schema = 'public'

    # Table을 Truncate하고 새로 Insert합니다
    df.to_sql(
        name = dst_table,
        schema = dst_schema,
        if_exists = 'replace',
        con=dst_engine
    )


migrate_data_task = PythonOperator(
    task_id='extract_load',
    python_callable=migrate_data,
    provide_context=True,
    dag=dag,
)
