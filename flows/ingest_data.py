from from_web_to_gcs import from_web_to_gcs
from from_gcs_to_bq import from_gcs_to_bq
from run_dbt_job import dbt_job_flow 
from prefect import flow, task


@flow()
def ingest_data():
    """Main flow to ingest data from web into Big Query"""

    # download dataset from the Eurostat and store in in the GCS bucket
    from_web_to_gcs()

    # Upload this dataset in the BigQuery
    from_gcs_to_bq()
    
    #You can't use the dbt Cloud API in the dbt Cloud Free pricing plan.
    # So, the corresponding dbt job should be run in dbt Cloud UI mannually
    # run_dbt_job()



if __name__ == "__main__":
    ingest_data()
