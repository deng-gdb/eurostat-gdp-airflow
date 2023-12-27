from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
import os.path
import sys
from prefect.blocks.system import Secret


@task(retries=3)
def download_from_gcs(file_name: str) -> Path:
    """Download data from GCS bucket to the working directory"""

    gcs_block = GcsBucket.load("eurostat-gdp-gcs-bucket")

    # https://prefecthq.github.io/prefect-gcp/cloud_storage/#prefect_gcp.cloud_storage.GcsBucket.get_directory
    gcs_block.get_directory(local_path = os.path.dirname(__file__))

    path = Path(os.path.join(os.path.dirname(__file__), file_name))

    return path


@task()
def upload_to_bq(path: Path, table_name: str) -> None:
    """Upload DataFrame to BiqQuery"""

    # read csv file in the dataframe
    df = pd.read_csv(path)

    # get gcp credentials from the GcpCredentials Prefect block
    gcp_credentials_block = GcpCredentials.load("eurostat-gdp-gcp-creds")

    # get gcp project_id value from the Secret Prefect block
    secret_block = Secret.load("project-id")

    # upload the dataframe to the BigQuery
    # if the destination table doesn't exisit - it will be created 
    # https://pandas-gbq.readthedocs.io/en/latest/api.html#pandas_gbq.to_gbq
    df.to_gbq(
        destination_table=table_name,
        project_id=secret_block.get(),
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500000,
        if_exists="replace",
    )


@flow()
def from_gcs_to_bq():
    """Main flow to load data into Big Query"""

    bq_table_name = 'eurostat_gdp_raw.nama-10r-2gdp'
    file_name = 'eurostat_gdp.csv'
    
    path = download_from_gcs(file_name)

    upload_to_bq(path, bq_table_name)

