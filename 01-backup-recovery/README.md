# GCP Automated Backup and Recovery System

## 1. Project Overview

This project demonstrates a Python-based backup and recovery system built using Google Cloud Platform (GCP).

The solution uses Google Cloud Storage to store backup files, Python to perform backup and recovery operations, Docker to package the application, Cloud Build to build container images, Artifact Registry to store images, and Cloud Run Jobs to execute backup tasks.

Cloud Scheduler was configured and successfully tested to trigger Cloud Run Jobs automatically. The temporary Scheduler job was deleted after testing.

### Project Objectives

- Automate backup operations using Python.
- Store backup files securely in Cloud Storage.
- Maintain previous file versions using Object Versioning.
- Containerize the backup application using Docker.
- Build and store container images using Cloud Build and Artifact Registry.
- Execute backup tasks using Cloud Run Jobs.
- Schedule automated execution using Cloud Scheduler.
- Monitor execution through Cloud Logging.
- Restore previous file versions using generation IDs.

## 2. Architecture

![GCP Automated Backup and Recovery Architecture](https://github.com/user-attachments/assets/74fda5cd-4aa2-4150-a560-1c1ebf1a0bdb)

### Automated Backup Workflow

Cloud Scheduler → Cloud Run Jobs API → Cloud Run Job → Docker Container → Python Backup Script → Cloud Storage → Cloud Logging

### Recovery Workflow

Cloud Storage → Object Versioning → Object Generation ID → restore.py → Recovered File

![Backup Recovery Architecture](docs/architecture-recovery.png)

## 3. Technologies Used

| Category | Technology |
|---|---|
| Cloud Platform | Google Cloud Platform |
| Object Storage | Cloud Storage |
| Containerization | Docker |
| Container Registry | Artifact Registry |
| Container Build | Cloud Build |
| Container Execution | Cloud Run Jobs |
| Scheduling | Cloud Scheduler |
| Programming | Python 3.12 |
| Python Library | google-cloud-storage |
| Identity and Access | IAM and Service Accounts |
| Monitoring | Cloud Logging |
| Version Control | Git and GitHub |

## 4. GCP Project Configuration

| Configuration | Value |
|---|---|
| GCP Region | us-central1 |
| Artifact Registry | gcp-backup-repo |
| Docker Image | backup-job:v1 |
| Cloud Run Job | backup-job |
| Cloud Scheduler | daily-backup-trigger |
| Storage Bucket | project-04354dfd-b58a-4510-a66-backup |
| Backup Object | sample.txt |

The project uses a single GCP region, us-central1.

## 5. Project Implementation

### 5.1 Configure GCP Project

Set the active GCP project:

```bash
gcloud config set project PROJECT_ID
```

Verify the active project:

```bash
gcloud config get-value project
```

Configure the default region:

```bash
gcloud config set compute/region us-central1
```

### 5.2 Enable Required GCP APIs

Enable the required services:

```bash
gcloud services enable storage.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

These APIs provide access to Cloud Storage, Cloud Run, Cloud Scheduler, Cloud Build and Artifact Registry.

### 5.3 Create Cloud Storage Bucket

Create the backup bucket:

```bash
gcloud storage buckets create gs://BUCKET_NAME \
  --location=us-central1 \
  --default-storage-class=STANDARD \
  --uniform-bucket-level-access
```

Enable public access prevention:

```bash
gcloud storage buckets update gs://BUCKET_NAME \
  --public-access-prevention
```

Enable Object Versioning:

```bash
gcloud storage buckets update gs://BUCKET_NAME \
  --versioning
```

Verify bucket configuration:

```bash
gcloud storage buckets describe gs://BUCKET_NAME
```

List stored objects:

```bash
gcloud storage ls gs://BUCKET_NAME
```

List all object generations:

```bash
gcloud storage ls --all-versions gs://BUCKET_NAME/sample.txt
```

Purpose:

- Cloud Storage provides durable object storage.
- Object Versioning preserves previous generations when an object is overwritten.
- Uniform bucket-level access uses IAM instead of individual object ACLs.
- Public access prevention blocks public access to bucket data.

### 5.4 Develop Python Backup Script

The project uses the Google Cloud Storage Python client library.

Install dependencies:

```bash
pip install -r requirements.txt
```

The backup script performs these operations:

1. Imports the required Python libraries.
2. Initializes the Cloud Storage client.
3. Connects to the destination bucket.
4. Generates timestamped backup content.
5. Uploads the file as sample.txt.
6. Records execution details using Python logging.
7. Handles exceptions during execution.

Run the local backup script:

```bash
python3 backup.py
```

When running inside Cloud Run, the script writes logs to stdout. Cloud Logging collects container logs automatically.

### 5.5 Python Backup Recovery

The recovery script downloads an earlier object generation using its generation ID.

List available versions:

```bash
gcloud storage ls --all-versions gs://BUCKET_NAME/sample.txt
```

Before running restore.py, set the generation ID of the version you want in the script.

Execute the recovery script:

```bash
python3 restore.py
```

Verify the recovered content:

```bash
cat restored_sample.txt
```

Purpose:

Object generations identify individual versions of an object. The recovery script uses the selected generation ID to download an earlier version.

### 5.6 Docker Containerization

Created a Dockerfile using Python 3.12-slim.

The Dockerfile:

- Defines the base Python image.
- Sets the application working directory.
- Copies requirements.txt.
- Installs Python dependencies.
- Copies backup.py.
- Executes the backup application.

Local build (optional, for testing). The deployed image was built with Cloud Build in section 5.7.

```bash
docker build -t backup-job:v1 .
```

List local Docker images:

```bash
docker images
```

### 5.7 Cloud Build and Artifact Registry

Create an Artifact Registry Docker repository:

```bash
gcloud artifacts repositories create gcp-backup-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="GCP automated backup Docker images"
```

Build and push the Docker image using Cloud Build:

```bash
gcloud builds submit \
  --tag us-central1-docker.pkg.dev/PROJECT_ID/gcp-backup-repo/backup-job:v1
```

Cloud Build performs the following operations:

1. Uploads the source files.
2. Builds the Docker image.
3. Installs the required dependencies.
4. Creates the container image.
5. Pushes the image to Artifact Registry.

List stored images:

```bash
gcloud artifacts docker images list \
  us-central1-docker.pkg.dev/PROJECT_ID/gcp-backup-repo
```

### 5.8 Configure IAM and Service Accounts

Create the Cloud Run Job service account:

```bash
gcloud iam service-accounts create backup-job-sa \
  --display-name="Backup Job Service Account"
```

Grant Cloud Storage object permissions:

```bash
gcloud storage buckets add-iam-policy-binding gs://BUCKET_NAME \
  --member="serviceAccount:backup-job-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectUser"
```

The backup service account receives object-level access to the backup bucket.

### 5.9 Deploy Cloud Run Job

Create the Cloud Run Job:

```bash
gcloud run jobs create backup-job \
  --image=us-central1-docker.pkg.dev/PROJECT_ID/gcp-backup-repo/backup-job:v1 \
  --region=us-central1 \
  --service-account=backup-job-sa@PROJECT_ID.iam.gserviceaccount.com \
  --memory=512Mi \
  --task-timeout=300s
```

Execute the Cloud Run Job:

```bash
gcloud run jobs execute backup-job \
  --region=us-central1 \
  --wait
```

List executions:

```bash
gcloud run jobs executions list \
  --job=backup-job \
  --region=us-central1
```

Describe the job:

```bash
gcloud run jobs describe backup-job \
  --region=us-central1
```

Cloud Run Jobs execute containerized tasks and stop after the task completes.

### 5.10 Configure Cloud Scheduler

Cloud Scheduler was configured to trigger the Cloud Run Job using an authenticated HTTP request.

Create the Scheduler service account:

```bash
gcloud iam service-accounts create scheduler-invoker \
  --display-name="Cloud Scheduler Invoker"
```

Grant permission to invoke the Cloud Run Job:

```bash
gcloud run jobs add-iam-policy-binding backup-job \
  --region=us-central1 \
  --member="serviceAccount:scheduler-invoker@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
```

Create the Scheduler job:

```bash
gcloud scheduler jobs create http daily-backup-trigger \
  --location=us-central1 \
  --schedule="10 16 * * *" \
  --time-zone="Asia/Kolkata" \
  --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/PROJECT_ID/jobs/backup-job:run" \
  --http-method=POST \
  --message-body="{}" \
  --oauth-service-account="scheduler-invoker@PROJECT_ID.iam.gserviceaccount.com" \
  --oauth-token-scope="https://www.googleapis.com/auth/cloud-platform"
```

The schedule `10 16 * * *` means daily at 4:10 PM.

Describe Scheduler configuration:

```bash
gcloud scheduler jobs describe daily-backup-trigger \
  --location=us-central1
```

List Cloud Run executions:

```bash
gcloud run jobs executions list \
  --job=backup-job \
  --region=us-central1
```

The scheduled execution was successfully tested and verified. The temporary Scheduler job was deleted after testing.

```bash
gcloud scheduler jobs delete daily-backup-trigger \
  --location=us-central1
```

See [CLOUD-SCHEDULER.md](CLOUD-SCHEDULER.md) for the detailed Scheduler workflow and configuration.

### 5.11 Cloud Logging

Cloud Run container logs are collected in Cloud Logging.

Check backup logs:

```bash
gcloud logging read \
  'resource.type="cloud_run_job" AND resource.labels.job_name="backup-job"' \
  --project=PROJECT_ID \
  --limit=20 \
  --freshness=2h
```

Expected application messages include:

```text
Backup started
Backup uploaded successfully
Bucket: BUCKET_NAME
Object: sample.txt
```

These logs help verify backup execution and troubleshoot failures.

## 6. Prerequisites

Before recreating the project, prepare:

- A GCP project with billing enabled.
- Cloud Shell or gcloud CLI.
- Python 3.12.
- Docker for optional local image testing.
- Permissions to create buckets, service accounts, Artifact Registry repositories and Cloud Run Jobs.
- The backup bucket name configured in backup.py.
- The required Python dependencies in requirements.txt.

Cloud Run uses its attached service account for authentication. Local execution requires suitable Google Cloud credentials and IAM permissions.

## 7. Complete Deployment Workflow

The following is the recommended deployment order for recreating the automated application.

1. Create or select the GCP project.
2. Enable the required APIs.
3. Create the Cloud Storage bucket.
4. Configure Object Versioning.
5. Develop and test the Python backup script.
6. Develop and test the recovery script.
7. Create the Dockerfile.
8. Create the Artifact Registry repository.
9. Build and push the image using Cloud Build.
10. Create the backup service account.
11. Grant bucket permissions.
12. Deploy the Cloud Run Job.
13. Execute the Cloud Run Job.
14. Verify the uploaded object.
15. Inspect Cloud Logging.
16. Create the Scheduler service account.
17. Grant Cloud Run invocation permission.
18. Create and test the Cloud Scheduler job.
19. Verify the scheduled execution.
20. Remove the temporary Scheduler after testing.

## 8. IAM and Security

Dedicated service accounts were used to separate backup execution from scheduled invocation.

| Service Account | IAM Role | Purpose |
|---|---|---|
| backup-job-sa | roles/storage.objectUser | Upload and manage backup objects |
| scheduler-invoker | roles/run.invoker | Invoke the Cloud Run Job |

Security configurations:

- Uniform bucket-level access.
- Public access prevention.
- Dedicated service accounts.
- Least-privilege IAM permissions.
- OAuth authentication for Scheduler.

The Cloud Scheduler service agent also requires the appropriate service-agent permissions for Cloud Run integration.

## 9. Troubleshooting

| Problem | Resolution |
|---|---|
| Authentication failure | Check active gcloud account and credentials |
| Permission denied during upload | Check backup service account bucket IAM permissions |
| Cloud Build staging bucket error | Check Cloud Build service account permissions |
| Artifact Registry push failure | Check Artifact Registry Writer permissions |
| Cloud Run execution failure | Inspect execution status and Cloud Logging |
| Scheduler invocation failure | Check OAuth identity and roles/run.invoker |
| Restore failure | Verify the object generation ID |
| Missing logs | Check resource type and time range in Cloud Logging |

## 10. Project Screenshots

### Cloud Storage and Object Versioning

![Cloud Storage Bucket](screenshots/01-storage-bucket.png)

![Object Versioning](screenshots/03-object-versioning.png)

### Backup and Recovery

![File Recovery](screenshots/04-file-recovery.png)

![Backup Logging](screenshots/05-backup-logging.png)

### Artifact Registry and Cloud Run

![Artifact Registry](screenshots/07-artifact-registry.png)

![Cloud Run Job Execution](screenshots/09-cloud-run-job-success.png)

### Cloud Scheduler and Cloud Logging

![Cloud Scheduler Execution](screenshots/10-cloud-scheduler-success.png)

![Cloud Logging](screenshots/11-cloud-logging.png)

### Backup Object Metadata

![Backup Object Metadata](screenshots/12-backup-object-metadata.png)

## 11. Repository Structure

```text
01-backup-recovery/
│
├── backup.py
├── restore.py
├── requirements.txt
├── Dockerfile
├── README.md
├── CLOUD-SCHEDULER.md
│
├── docs/
│   ├── architecture-automated.png
│   └── architecture-recovery.png
│
└── screenshots/
    ├── 01-storage-bucket.png
    ├── 02-backup-upload.png
    ├── 03-object-versioning.png
    ├── 04-file-recovery.png
    ├── 05-backup-logging.png
    ├── 06-github-project-files.png
    ├── 07-artifact-registry.png
    ├── 08-docker-build-success.png
    ├── 09-cloud-run-job-success.png
    ├── 10-cloud-scheduler-success.png
    ├── 11-cloud-logging.png
    └── 12-backup-object-metadata.png
```

## 12. What I Learned

- Creating and configuring GCP resources.
- Working with Cloud Storage buckets and Object Versioning.
- Writing Python scripts for cloud backup and recovery.
- Building Docker images for cloud workloads.
- Using Cloud Build to build and publish container images.
- Managing container images through Artifact Registry.
- Executing containerized workloads using Cloud Run Jobs.
- Configuring dedicated service accounts.
- Applying least-privilege IAM permissions.
- Connecting Cloud Scheduler to the Cloud Run Jobs API.
- Troubleshooting Cloud Build permission errors.
- Monitoring cloud workloads through Cloud Logging.
- Recovering earlier object generations using Python.

## 13. Future Improvements

- Configure lifecycle rules to remove old noncurrent object versions and control storage costs.
- Add Cloud Monitoring alert policies for failed backup executions.
- Implement Infrastructure as Code using Terraform.
- Implement CI/CD using GitHub Actions.
- Add automated backup integrity verification.
- Add configurable backup retention policies.
- Extend the application to support multiple backup files and directories.

## 14. Cleanup and Cost Management

Delete resources after completing the project demonstration.

Delete the Cloud Run Job:

```bash
gcloud run jobs delete backup-job \
  --region=us-central1
```

Delete the Artifact Registry repository:

```bash
gcloud artifacts repositories delete gcp-backup-repo \
  --location=us-central1
```

Delete the Cloud Storage bucket and all its objects and versions:

```bash
gcloud storage rm -r gs://BUCKET_NAME
```

Delete the backup service account:

```bash
gcloud iam service-accounts delete \
  backup-job-sa@PROJECT_ID.iam.gserviceaccount.com
```

Delete the Scheduler service account:

```bash
gcloud iam service-accounts delete \
  scheduler-invoker@PROJECT_ID.iam.gserviceaccount.com
```

The Scheduler job was already deleted after testing.

Check for remaining resources in Cloud Run, Artifact Registry, Cloud Storage, Compute Engine and other services before considering cleanup complete.

Deleting a bucket removes all its stored objects and versions. Confirm you no longer need the backups before running the deletion command.

## 15. Project Outcome

Built and tested a containerized Python backup and recovery application using Google Cloud Platform.

Successfully verified:

- Python backup uploads to Cloud Storage.
- Cloud Storage Object Versioning.
- Recovery using object generation IDs.
- Docker image creation and publishing.
- Cloud Build execution.
- Cloud Run Job execution.
- Cloud Scheduler triggering.
- IAM-based service account permissions.
- Centralized execution logs through Cloud Logging.

Cloud Scheduler was tested successfully and deleted after testing. The source code and project documentation are retained in GitHub.

## Author

GitHub: https://github.com/nishchiashok14
