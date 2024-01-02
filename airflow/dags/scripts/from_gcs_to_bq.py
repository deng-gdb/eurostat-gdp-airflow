import pandas as pd
import sys
from google.oauth2 import service_account


def upload_to_bq(*args) -> None:
    """Upload DataFrame to BiqQuery
    :param 0: source path & file-name
    :param 1: GCP credentials
    :param 2: GCP project ID
    :param 3: BQ table name
    
    """

    source_file_name = args[0]
    gcp_credentials = args[1]
    gcp_project_id = args[2]
    bq_table_name = args[3]

    # read csv file in the dataframe
    df = pd.read_csv(source_file_name)

    # get google service account credentials
    # Ref: https://google-auth.readthedocs.io/en/latest/user-guide.html
    credentials = service_account.Credentials.from_service_account_file(gcp_credentials)

    # upload the dataframe to the BigQuery
    # if the destination table doesn't exisit - it will be created 
    # Ref: https://pandas-gbq.readthedocs.io/en/latest/api.html#pandas_gbq.to_gbq
    # (alternative approach: https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv)
    df.to_gbq(
        destination_table=bq_table_name,
        project_id=gcp_project_id,
        credentials=credentials,
        chunksize=500000,
        if_exists="replace",
    )


if __name__ == "__main__":
    args = sys.argv

    result = globals()[args[1]](*args[2:])
    print(result)