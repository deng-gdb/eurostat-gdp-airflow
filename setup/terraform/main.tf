terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region = var.region
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# Data Lake Bucket
resource "google_storage_bucket" "bucket" {
  name          = "${var.data_lake_bucket}_${var.gcp_project_id}" # Concatenating DL bucket & Project name for unique naming
  location      = var.region

  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

# DWH
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.raw_bq_dataset
  project    = var.gcp_project_id
  location   = var.region
}

# Artifact registry for containers
resource "google_artifact_registry_repository" "artifact-repository" {
  location      = var.region
  repository_id = var.registry_id
  format        = "DOCKER"
}

# Compute Engine VM Instance

resource "google_compute_instance" "default" {
  name         = "eurostat-gdp-vm-instance"
  machine_type = "e2-micro"
  zone         = "us-east1-b"

  boot_disk {
    initialize_params {
      image = "ubuntu-2004-focal-v20230918"
      size = "30"
      type="pd-standard"
      
    }
  }

  network_interface {
    network = "default"

    access_config {
      # Associate the public IP address to this instance
      nat_ip = google_compute_address.static.address
      network_tier = "PREMIUM"
    }
  }

  # Connect to the instance via Terraform and remotely execute the script using SSH
  provisioner "remote-exec" {
    script = var.vm_script_path

    connection {
      type        = "ssh"
      host        = google_compute_address.static.address
      user        = var.ssh_user_name
      private_key = file(var.ssh_private_key_path)
    }
  }

  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = var.ce_service_account_email
    scopes = ["cloud-platform"]
  }

}

# Create a public IP address for the google compute instance to utilize
resource "google_compute_address" "static" {
  name = "vm-public-ip-address"
}