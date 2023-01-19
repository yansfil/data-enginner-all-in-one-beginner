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
    'transform_order_items',
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
    catchup=False,
)

def transform_data(ds, **kwargs):
    hook = PostgresHook(postgres_conn_id='dst_db_connection')
    src_table = 'public.order_items'

    df = hook.get_pandas_df(
        f"""
            SELECT to_char(date_trunc('month', oi.created_at), 'yyyy-mm') as date, sum(oi.sale_price) as total_revenue, count(distinct oi.order_id) as total_cnt
            FROM {src_table} oi 
            WHERE oi.created_at is not NULL
            GROUP BY date_trunc('month', oi.created_at)
            ORDER BY 1
        """)

    dst_engine = hook.get_sqlalchemy_engine()
    dst_table = 'monthly_revenue'
    dst_schema = 'public'

    # Table을 Truncate하고 새로 Insert합니다
    df.to_sql(
        name = dst_table,
        schema = dst_schema,
        if_exists = 'replace',
        con=dst_engine,
        index=False
    )


migrate_data_task = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)
