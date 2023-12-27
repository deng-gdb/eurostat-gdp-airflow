from pathlib import Path
import pandas as pd
from prefect import flow, task, get_run_logger
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
import os.path
import sys


@task(name="log-get-table-schema-task")
def get_table_schema(config_path: str) -> pd.DataFrame:
    """Read the BigQuery table schema from the configuration"""
    
    # read the BigQuery table schema from the configuration
    table_schema_path = os.path.abspath(config_path)
    #print(table_schema_path)
    logger = get_run_logger()
    logger.info(table_schema_path)
    df_table_schema = pd.read_json(table_schema_path, orient='records')
    #df_table_schema = pd.DataFrame()

    return df_table_schema


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read data from Eurostat web into pandas DataFrame"""

    df = pd.read_table(dataset_url)
    return df


@task()
def transform(df: pd.DataFrame, table_schema: pd.DataFrame) -> pd.DataFrame:
    """Transform input DataFrame accordingly"""

    # remove from the dataframe the first row which contains the initial column names
    df_transformed = df.drop(index=0)

    # split the first column of the dataframe into 3 separate columns
    df1 = df_transformed['freq,unit,geo\TIME_PERIOD'].str.split(",",expand=True)
    
    # insert second and third splitted columns in the specified positions in the dataframe
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.insert.html
    df_transformed.insert(1, 'string_field_0', df1[1])
    df_transformed.insert(2, 'string_field_1', df1[2])

    # drop the first column of the dataframe
    df_transformed = df_transformed.drop(df_transformed.columns[0], axis=1)
      
    # prepare the dataframe to be inserted in the BigQuery table.  
    # in accordance with the official documentation, the dataframe must contain fields 
    # (matching name and type) currently in the destination table.
    # see details in https://pandas-gbq.readthedocs.io/en/latest/writing.html#writing-to-an-existing-table 

    # create a list, which contains the field names from the configuration
    field_names_list = table_schema['name'].values.tolist()

    # rename dataframe column names in accordance with the BigQuery table schema from the configuration
    df_transformed.columns = field_names_list

    return df_transformed


@task()
def write_local(df: pd.DataFrame, dataset_file_name: str) -> Path:
    """Write DataFrame out locally as csv file"""

    path = Path(f"{dataset_file_name}.csv")
    df.to_csv(path)

    return path


@task()
def write_to_gcs_data_lake(path: Path) -> None:
    """Upload local csv file to GCS data lake bucket"""
    
    gcs_bucket_block = GcsBucket.load("eurostat-gdp-gcs-bucket")
    gcs_bucket_block.upload_from_path(from_path=path, to_path=path)
    
    return
       

@flow(log_prints=True)
def from_web_to_gcs() -> None:
    """The main ingest function"""

    dataset_name = "NAMA_10R_2GDP"
    dataset_format = "TSV"
    dataset_url = f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{dataset_name}?format={dataset_format}&compressed=false"
    dataset_file_name = "eurostat_gdp"
    file_path = '../setup/table_schema.json'
    config_path = Path(os.path.join(os.path.dirname(__file__), file_path))

    bq_table_name = 'eurostat_gdp_raw.nama-10r-2gdp'

    table_schema = get_table_schema(config_path)
    
    # fetch dataset from the eurostat site and put it into dataframe
    df = fetch(dataset_url)
    df = df.astype(str)

    # make the required transformations for the fetched dataframe
    df_transformed = transform(df, table_schema)
   
    # Write DataFrame out locally as csv file
    path = write_local(df_transformed, dataset_file_name)

    # Upload local csv file to GCS data lake bucket
    write_to_gcs_data_lake(path)
    
