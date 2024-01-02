variable "gcp_project_id" {
  description = "Your GCP Project ID"
}

variable "ce_service_account_email" {
  description = "Your GCP Compute Engine Service Account email"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "us-east1"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "data_lake_bucket" {
  description = "The name of the Cload Storage bucket which is used as a Data Lake"
  type = string
  default = "eurostat_gdp_data_lake"
}

variable "raw_bq_dataset" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "eurostat_gdp_raw"
}

variable "registry_id" {
  type = string
  description = "Name of artifact registry repository."
  default = "eurostat-gdp-repository"
}

variable "vm_script_path" {
  type        = string
  description = "The path to the script locally on the machine, which Terraform run on the created VM"
  default = "scripts/install.sh"
}

variable "ssh_user_name" {
  type        = string
  description = "The name of the user that will be used to remote exec the script trough ssh"
}

variable "ssh_private_key_path" {
  type        = string
  description = "The path to the private ssh key used to connect to the instance"
}

