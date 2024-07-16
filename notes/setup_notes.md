# 1. Create a GCP project

- To create a new Google Cloud project go to the [GCP dashboard](https://console.cloud.google.com/) and create a new project.
- After you have created the project, you need to create a _Service Account_ in the project: 
  - ***IAM & Admin -> Service Accounts -> Create Service Account***
  - Enter the following information:
    - _***Service Account ID***_. Provide `your own value` or hit `Generate` link.
    - Grant this service account access to the project with the following roles:
      - `BigQuery Admin`
      - `BigQuery Job User`
      - `Storage Admin`
      - `Storage Object Admin`
      - `Cloud Run Admin`
      - `Service Account User`
      - `Secret Manager Admin`
      - `Viewer`
      - `Editor`
- After that create the Service Account credentials file.
  - **Service Account** -> **Manage Keys** -> **Add Key** -> **Create new key**  
  - Chose Key type: `JSON`
- Download the created Service Account credentials file to the **local machine** and store it in your home folder, i.e. in the `$HOME/.google/`.
- Create an environment variable `GOOGLE_APPLICATION_CREDENTIALS` on the **local machine** and assign to it the path to the your json Service Account credentials file
  - Open your .bashrc file: `nano .bashrc`
  - At the end of the file, add the following row: `export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.google/<your_credentials>.json"`  
  - Save you changes and close nano: `ctrl+O, ctrl+X`
  - Log out of your current terminal session and log back in, or run `source ~/.bashrc` to activate the environment variable.
- Then activate the following APIs in your GCP project:  
  - [Identity and Access Management (IAM) API](https://console.cloud.google.com/apis/library/iam.googleapis.com)
  - [IAM Service Account Credentials API](https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com)
  - [Compute Engine API](https://console.cloud.google.com/apis/library/compute.googleapis.com)
  - [Artifact Registry API](https://console.cloud.google.com/apis/library/artifactregistry.googleapis.com)
  - [Cloud Storage API](https://console.cloud.google.com/apis/library/storage.googleapis.com)
  - [BigQuery API](https://console.cloud.google.com/apis/library/bigquery.googleapis.com)
  - [Cloud Run API](https://console.cloud.google.com/apis/library/run.googleapis.com)

# 2. Setup local development environment

## 2.1 Install and setup Google Cloud SDK on local machine

- Download the Google Cloud SDK from [this link](https://cloud.google.com/sdk/docs/install-sdk#linux) and install it.
- Initialize the SDK by following [these instructions.](https://cloud.google.com/sdk/docs/install-sdk)
  - Run `gcloud init` from a terminal and follow the instructions:
    - The system will generate a link and ask you to go to the link in your browser.
    - When you go to this link, Google will generate the verification code in gcloud CLI on the machine you want to log into.
    - Copy this code and paste it into your terminal window prompt. 
  - Make sure that your project is selected with the command `gcloud config list`.
 
## 2.2 Clone the project repo on local machine

- Fork this GitHub repository in your GitHub account and clone the forked repo. It is requred because you should perform some customization changes in the code.  
- Go to the your `$HOME` directory.
- Run the following command: `git clone https://github.com/<your-git-account-name>/eurostat-gdp.git`

## 2.3 Install Airflow on local machine

1. Go to the `eurostat-gdp-airflow/airflow` and update `docker-compose.yaml` file.
  - under the section `x-airflow-common:`
  - update the env variable `GOOGLE_APPLICATION_CREDENTIALS`. Replace <google_credentials.json> value by your own credentials file name. It is supposed that your credentials file laid in the /.google folder.
  - update the env variable `GCP_PROJECT_ID`. Replace <gcp_project_id> value by your own project_id value.
  - update the env variable `GCP_GCS_BUCKET`. Replace <gcs_bucket_name> value by your own gcs_bucket_name value. It is supposed that the bucket name should be in the format: `eurostat_gdp_data_lake_<your_gcp_project_id>`.
2. Run Docker Desktop
3. `cd eurostat-gdp-airflow/airflow`
4. Build the image. It may take several minutes You only need to do this the first time you run Airflow or if you modified the Dockerfile or the `requirements.txt` file.
    ```bash
    docker-compose build
    ```
5. Initialize Airflow environment:
    ```bash
    docker-compose up airflow-init
    ```
6. Run Airflow
    ```bash
    docker-compose up -d
    ```
7. You may now access the Airflow GUI by browsing to `localhost:8080`. Username and password are both `airflow` .
>***IMPORTANT***: this is ***NOT*** a production-ready setup! The username and password for Airflow have not been modified in any way; you can find them by searching for `_AIRFLOW_WWW_USER_USERNAME` and `_AIRFLOW_WWW_USER_PASSWORD` inside the `docker-compose.yaml` file.

## 2.4 Install Terraform on local machine

- Terraform client installation: [https://www.terraform.io/downloads](https://www.terraform.io/downloads)  
  - `wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg`
  - `echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list`
  - `sudo apt update && sudo apt install terraform`
- Check that Terraform installed successfully. Run: `terraform -version`

## 2.5 Set up SSH access to the Compute Engine VM instances on local machine

- **Create an SSH key pair on local machine.**  
  - If you connect to GCP Compute Engine virtual machine (VM) instances using third party tools or OpenSSH, you need to add a key to your VM before you can connect. If you don't have an SSH key, you must create one.
  - Create SSH key pair in accordance with the following GCP guidance: [Create SSH keys](https://cloud.google.com/compute/docs/connect/create-ssh-keys)  
    - Open a terminal window and run the following command: `ssh-keygen -t rsa -f ~/.ssh/<key_file_name> -C <user_name> -b 2048`, where:   
      - <key_file_name>: the name for your SSH key file, replace it by your own value  
      - <user_name>: your username on the VM, replace it by your own value  
    - This comand will create two files in the .ssh folder: <key_file_name> (private key) and <key_file_name>.pub (public key)
- **Upload the created ssh public key to GCP Compute Engine.**     
  - Copy the content of the <key_file_name>.pub  
  - Go to the your `GCP project console -> Compute Engine -> Settings -> Metadata -> SSH keys -> Add SSH Key`.
  - Insert the copied content of the <key_file_name>.pub -> Save.
  - All instances in this project will use this ssh key.
- **Cnfigure SSH access on the local machine.**
  - Make sure that the gcloud SDK is configured for your project:
    - Run `gcloud config list` to see your active gcp configuration details.
    - If you have multiple google accounts but the active configuration does not match the account you want - run the following command: `gcloud config configurations activate my-account`
    - If the active configuration matches your account but points to a different project - run the following command: `gcloud config set project my-project`
  - Start the created VM instance in the Google Cloud dashboard.
  - Go to the ~/.ssh folder and run `gcloud compute config-ssh`
    - This comand creates `~/.ssh/config` file for your ssh gcp connection
    - If you did not have already a SSH key, a pair of public and private SSH keys, this command will create them.
    - The output of this command will provide you the host name for the ssh connection to your instance in the format: `<instance>.<zone>.<project>`.
    - Now you should be able to open the SSH connection to your VM instance: `ssh <instance>.<zone>.<project>`
  - **You should run this command** `gcloud compute config-ssh` **each time when your VMs instances are stopped and started again** in order to update `~/.ssh/config` file and set up new value for External IP for your instance. This IP is changed every time when the instance stopped and restart again.
  - Thease are some other usefull gcloud SDK commands:
    - `gcloud compute instances list` - provides a list of your available instances
    - `gcloud compute instances start <instance_name>` - starts your instance
    - `gcloud compute instances stop <instance_name>` - stops your instance

# 3. Create GCP project infrastructure with Terraform

Run the following commands:
- `cd ~/eurostat-gdp-airflow/terraform`
- edit a file `terraform.tfvars` - insert your own values for the variables here.
- `terraform init`
- `terraform plan`
- `terraform apply`
- Go to the your GCP dashboard and make sure that the following resourses were created:
  - [Cloud Storage bucket](https://console.cloud.google.com/storage): `eurostat_gdp_data_lake_<your_gcp_project_id>`
  - [BigQuery dataset](https://console.cloud.google.com/bigquery): `eurostat_gdp_raw`

# 4. Set up dbt environment

The dbt environment set up details you can find [here.](./dbt_notes.md)
