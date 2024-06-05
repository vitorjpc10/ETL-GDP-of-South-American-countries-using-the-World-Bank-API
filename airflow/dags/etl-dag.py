# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
# from datetime import datetime, timedelta
# from scripts.data_extraction import extract
# from scripts.data_transformation import transform
# from scripts.data_loading import load
#
# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2023, 6, 1),
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }
#
# dag = DAG(
#     dag_id='etl_pipeline',
#     default_args=default_args,
#     description='ETL pipeline for weather and traffic data',
#     schedule_interval=timedelta(days=1),
# )
#
# extract_task = PythonOperator(
#     task_id='extract',
#     python_callable=extract,
#     dag=dag,
# )
#
# transform_task = PythonOperator(
#     task_id='transform',
#     python_callable=transform,
#     provide_context=True,
#     dag=dag,
# )
#
# load_task = PythonOperator(
#     task_id='load',
#     python_callable=load,
#     provide_context=True,
#     dag=dag,
# )
#
# extract_task >> transform_task >> load_task
