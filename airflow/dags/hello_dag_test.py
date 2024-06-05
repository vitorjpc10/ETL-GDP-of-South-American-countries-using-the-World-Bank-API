from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Uncomment these imports if needed
# from scripts.data_extraction import extract
# from scripts.data_transformation import transform
# from scripts.data_loading import load

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def hello_world():
    print("Hello world!")
    for i in range(0, 10):
        print(f"TEST {i}")

with DAG(
        dag_id='hello_pipeline',
        default_args=default_args,
        description='hello world',
        schedule_interval='@daily',
        catchup=False,  # Add this line to disable catchup
) as dag:
    hello_task = PythonOperator(
        task_id='hello',
        python_callable=hello_world,
    )

    hello_task
