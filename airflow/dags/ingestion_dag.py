import os
#import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.models.xcom_arg import XComArg
#from airflow.operators.python import PythonOperator

#from google.cloud import storage
#from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
#import pyarrow.csv as pv
#import pyarrow.parquet as pq

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
GCP_CRED = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
BQ_TABLE_NAME = 'eurostat_gdp_raw.nama-10r-2gdp-1'

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}


# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="ingestion_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    # Ref: https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/example_dags/example_xcom/index.html#module-airflow.example_dags.example_xcom
    # download the dataset from Provider
    download_from_web_task = BashOperator(
        task_id="download_from_web_task",       
        bash_command='result=$(python /opt/airflow/dags/scripts/from_web_to_gcs.py download_from_web)  && echo "$result"',
        cwd="/opt/airflow/dags/scripts",
        dag=dag
    )

    # upload the dataset to Google Cloud Storage
    upload_to_gcs_data_lake = BashOperator(
        task_id="upload_to_gcs_data_lake",    
        bash_command=f'python /opt/airflow/dags/scripts/from_web_to_gcs.py write_to_gcs_data_lake '
        f'{BUCKET} '
        f'{XComArg(download_from_web_task)} '
        f'{XComArg(download_from_web_task)} ',
        cwd="/opt/airflow/dags/scripts",
        do_xcom_push=False,
        dag=dag
    )

    # Upload Dataset to BiqQuery
    upload_to_bq = BashOperator(
        task_id="upload_to_bq",    
        bash_command=f'python /opt/airflow/dags/scripts/from_gcs_to_bq.py upload_to_bq '
        f'{XComArg(download_from_web_task)} '
        f'{GCP_CRED} '
        f'{PROJECT_ID} '
        f'{BQ_TABLE_NAME} ',
        cwd="/opt/airflow/dags/scripts",
        do_xcom_push=False,
        dag=dag
    )


    download_from_web_task >> upload_to_gcs_data_lake >> upload_to_bq