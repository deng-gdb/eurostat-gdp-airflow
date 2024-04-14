# Local Machine 

In the project architecture, a local machine is used in order to create the project infrastructure in the Cloud, to create a Docker image for the Airflow, and as a host for the Airflow.

So, on the local machine the following software should be installed:
- Python
- Google Cloud SDK
- Git
- Terraform 
- Docker

The details see in the section [Setup local development environment](#setup-local-development-environment).

# Cloud Infrastructure with Terraform

The GCP Cloud Infrastructure in the project was implemented using the Terraform.
The Cloud Infrastructure created by Terraform includes the following items:

- Cloud Storage bucket
- BigQuery dataset

Terraform configuration located in the repo by the path: `eurostat-gdp-airflow/terraform/`  
To get more details regarding the Terraform configuration files see [the official documentation](https://developer.hashicorp.com/terraform/language/modules/develop/structure).

The Terraform configuration in the project consists of the following files:

- **main.tf**. This file contains the main set of configuration for the project.
- **variables.tf**. This file contains the declarations for variables used in the Terraform configuration.
- **terraform.tfvars**. This file specifies the values for the Terraform variables from the file `variables.tf` which contain private information and should be provided during project setup individually.

Let's review these files briefly. 

## main.tf

This file consists of blocks. The syntax of these blocks you can review in the [Terraform official documentation](https://developer.hashicorp.com/terraform/language/resources/syntax).
- The first block **_terraform_** contains the minimal Terraform version required and the backend to be used.
- The block **_provider_** defines the service provider and the project information.
- The block **_resource "google_storage_bucket"_** defines all required information in order to create Google Cloud storage bucket resource. The structure of this block you can find in the official documentation [here](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket).
- The block **_resource "google_bigquery_dataset"_** defines all required information in order to create Google BigQuery dataset resource. The structure of this block you can find in the official documentation [here](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset).

## variables.tf

This file contains the declarations for Terraform variables. It contains blocks also. 
Each block contains the name of the variable, the type, description and a default value for the variable if required. 
In this project the values for the variables were assigned through the defalt values in this file. Meanwhile, there are [other approaches](https://developer.hashicorp.com/terraform/language/values/variables) exist.

- `variable "gcp_project_id"`. Your own GCP Project ID. The value for this variable is not specified. This value should be entered in the file `terraform.tfvars`.
- `variable "ce_service_account_email"`. This is email identifier for your default Service Accaount, which is used by the Compute Engine service. The value for this variable is not specified. This value should be entered in the file `terraform.tfvars`. 
- `variable "region"`. The value for this variable specified taking into account the GCP free tier requirements.
- `variable "data_lake_bucket"`. The value for this variable specified the name of the Cloud Storage bucket that should be created.
- `variable "raw_bq_dataset"`. The value for this variable specified the name of the BigQuery dataset that should be created.
  - Be aware that this value must be alphanumeric (plus underscores). 

## terraform.tfvars

This file specifies the values for the variables from the file `variables.tf` which contain private information and should be provided during project setup individually.

- `gcp_project_id`.  You can find this value on the your GCP Project Dashboard.
- `ce_service_account_email`. This value you can find in your GCP console: IAM & Admin -> Service Accounts. Find the account with the name "Compute Engine default service account" and take its email.

The guidance regarding the Terraform execution see in the corresponding section:  [Create GCP project infrastructure with Terraform](#create-gcp-project-infrastructure-with-terraform) 
