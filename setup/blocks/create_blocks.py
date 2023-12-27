from dotenv import load_dotenv
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from prefect.filesystems import GitHub
from prefect.blocks.system import Secret
from prefect_dbt.cli.credentials import DbtCliProfile
from prefect_dbt.cloud import DbtCloudCredentials
import os


load_dotenv()

# create gcp credentials block
credentials_block = GcpCredentials(
    service_account_info = os.environ.get("SERVICE_ACCOUNT_CREDENTIALS", "default")  
)
credentials_block.save("eurostat-gdp-gcp-creds", overwrite=True)

# create gcs bucket
bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("eurostat-gdp-gcp-creds"),
    bucket=os.environ.get("GCS_BUCKET_NAME", "default")
)
bucket_block.save("eurostat-gdp-gcs-bucket", overwrite=True)

# create GitHub block
gh_block = GitHub(
    name="eurostat-gdp-github", repository=os.environ.get("GITHUB_REPOSITORY_URL", "default")
)

gh_block.get_directory("flows") # specify a subfolder of repo where your flows code is located

gh_block.save("eurostat-gdp-github", overwrite=True)

# create Prefect Secret block with the name "project-id"
Secret(value=os.environ.get("GCP_PROJECT_ID", "default")).save(name="project-id", overwrite=True)


# create dbt Cloud credentials block
dbt_cloud = DbtCloudCredentials(
    account_id=os.environ.get("DBT_CLOUD_ACCOUNT_ID", 12345),
    api_key=os.environ.get("DBT_CLOUD_API_KEY", "default"),
)
dbt_cloud.save("dbt-cloud", overwrite=True)

