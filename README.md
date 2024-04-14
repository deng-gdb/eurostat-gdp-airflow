# Index

- [Dataset](#dataset)
- [Technologies and Tools](#technologies-and-tools)
- [Data Pipeline Architecture](#data-pipeline-architecture)
  - [Local Machine](#local-machine)
  - [Cloud Infrastructure with Terraform](#cloud-infrastructure-with-terraform)
  - [Orchestration](#orchestration)
- [Data Ingestion and Data Lake](#data-ingestion-and-data-lake)
- [Data Transformation and Data Warehouse](#data-transformation-and-data-warehouse)
- [Data Visualization](#data-visualization)
- [Set up project environment](#set-up-project-environment)
  - [Prerequisites](#prerequisites)
  - [Create a GCP project](#create-a-gcp-project)
  - [Setup local development environment](#setup-local-development-environment)
    - [Install and setup Google Cloud SDK on local machine](#install-and-setup-google-cloud-sdk-on-local-machine)
    - [Clone the project repo on local machine](#clone-the-project-repo-on-local-machine)
    - [Install Airflow on local machine](#install-airflow-on-local-machine)
    - [Install Terraform on local machine](#install-terraform-on-local-machine)
    - [Set up SSH access to the Compute Engine VM instances on local machine](#set-up-ssh-access-to-the-compute-engine-vm-instances-on-local-machine)
  - [Create GCP project infrastructure with Terraform](#create-gcp-project-infrastructure-with-terraform)
  - [Set up dbt environment](#set-up-dbt-environment)


# Overview

This project is related to the processing of the **Eurostat** dataset: `"Gross domestic product (GDP) at current market prices by NUTS 2 regions"`. Eurostat online data code of this dataset: _**NAMA_10R_2GDP**_.
- The dataset is available at this [link.](https://ec.europa.eu/eurostat/web/products-datasets/-/nama_10r_2gdp)
- Metadata regarding this dataset you can find [here.](https://ec.europa.eu/eurostat/cache/metadata/en/reg_eco10_esms.htm)
- API for dataset access description is available at this [link.](https://wikis.ec.europa.eu/display/EUROSTATHELP/Transition+-+from+Eurostat+Bulk+Download+to+API)
- The sourse of the Regions dimension you can find [here.](http://dd.eionet.europa.eu/vocabulary/eurostat/sgm_reg/view)
- The sourse of the Units dimension you can find [here.](http://dd.eionet.europa.eu/vocabulary/eurostat/unit/)


## Technologies and Tools

- Cloud: Google Cloud Platform
- Infrastructure as Code: Terraform
- Containerization: Docker
- Workflow Orchestration: Airflow
- Data Lake: Google Cloud Storage
- Data Warehouse: BigQuery
- Data Modeling and Transformations: dbt
- Data Visualization: Looker Studio
- Language: Python 


## Data Architecture

![project-architecture](./img/project_architecture.png)

The architecture details notes you can find [here.](./notes/architecture_notes.md)

## Data Visualization
[To Index](#index)

![dashboard_params](./img/dashboard_params.jpg)

The dashboard consist of tree pages: Table, Bar, Map.

**Table**:
![Table](./img/dashboard1_1.jpg)
**Bar**:
![Bar](./img/dashboard2_1.jpg)
**Map**:
![Map](./img/dashboard3_1.jpg)

- The dashboard used in this project was created in the Google Looker Studio. 
- The Looker Studio is treated in the project as Front-End visualization tool only. All table joins and other data modeling actions, required for the visualization, were made by the dbt Cloud.
- Due to the fact that Looker Studio Google Geo charts [doesn't support NUTs regions](https://support.google.com/looker-studio/answer/9843174#country&zippy=%2Cin-this-article), the "Map" page of the dashbord represents data for Country level regions only. The details regarding the NUTs regions you can find [here.](https://ec.europa.eu/eurostat/web/nuts/background)
- The dashbord is based on the dataset `eurostat_gdp_prod_core.facts_gdp_joined` from the corresponding `DB Prod` Data Warehouse environment.
- **The restricted (by login/password) link at the dashboard located** [**here.**](https://lookerstudio.google.com/reporting/5cb1caed-76fb-4a2f-bbd3-b9e2bb8269b1) This link is restricted in order to avoid additional charging.

# Prerequisites

The following items could be treated as prerequisites in order to reproduce the project:

- An active [GCP account.](https://cloud.google.com)
- Installed Docker Desktop
- (Optional) A SSH client. It is supposed that you are using a Terminal and SSH.

# How to Run This Project

1. Set up project environment. The details you can find in [this note](./notes/setup_notes.md). 

# Data Ingestion and Data Lake
[To Index](#index)

Data Ingestion stage comprise the following activities:
- Download the corresponding dataset from the **Eurostat site**.
- Upload this dataset into the Google Cloud Storage in the **Data lake**.
- Load this dataset form the Data Lake into the BigQuery dataset in the **Data Warehouse** in the schema that contains raw source data.  

Prerequisites: you should complete all required activities mentioned in the section [Set up project environment](#set-up-project-environment).

In order to fulfill the data ingestion stage, do the following:

- On the **local machine**:
  - Run Docker Desktop
  - `cd eurostat-gdp-airflow/airflow`
  - Run Airflow
    ```bash
    docker-compose up -d
    ```
  - Access the Airflow GUI by browsing to `localhost:8080`. Username and password are both `airflow` .
  - Run **ingestion_dag**
- In your Google Cloud project go to **Cloud Storage** and open the corresponding bucket. You should see the file `eurostat_gdp.csv` there.
- In your Google Cloud project go to **Big Query** and open the dataset `eurostat_gdp_raw`. You should see the table `nama-10r-2gdp` there.

# Data Transformation and Data Warehouse
[To Index](#index)

The project uses Google BigQuery as a **Data Warehouse**. 
During the Data Transformation stage the data is carried over through the various transformations from the Raw data schema to the production Data Warehouse schema.  
This process is implemented using the [dbt Cloud](https://www.getdbt.com/product/dbt-cloud).  

The Data Transformation implementation details, Data Warehouse Modeling guidance and the corresponding workflow you can find [here.](./notes/dbt_notes.md)




# Set up project environment
















  



## Create GCP project infrastructure with Terraform
[To Index](#index)

Run the following commands:
- `cd ~/eurostat-gdp-airflow/terraform`
- edit a file `terraform.tfvars` - insert your own values for the variables here.
- `terraform init`
- `terraform plan`
- `terraform apply`
- Go to the your GCP dashboard and make sure that the following resourses were created:
  - [Cloud Storage bucket](https://console.cloud.google.com/storage): `eurostat_gdp_data_lake_<your_gcp_project_id>`
  - [BigQuery dataset](https://console.cloud.google.com/bigquery): `eurostat_gdp_raw`

## Set up dbt environment
[To Index](#index)

The dbt environment set up details you can find [here.](./notes/dbt_notes.md)
