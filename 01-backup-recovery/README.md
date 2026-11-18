# GCP Automated Backup and Recovery System

## 1. Project Overview

This project demonstrates a Python-based automated backup and recovery system built using Google Cloud Platform (GCP).

The solution uses Google Cloud Storage to store backup files, Python to perform backup and recovery operations, Docker to containerize the application, Cloud Build to build container images, Artifact Registry to store images, and Cloud Run Jobs to execute backup tasks.

Cloud Scheduler was configured and successfully tested to trigger Cloud Run Jobs automatically. The temporary Scheduler job was deleted after testing.

The project demonstrates cloud storage, containerization, IAM, automation, versioning, recovery, and centralized logging.

## 2. Architecture

![GCP Automated Backup and Recovery Architecture](https://github.com/user-attachments/assets/74fda5cd-4aa2-4150-a560-1c1ebf1a0bdb)

### Architecture Workflow

Cloud Scheduler → Cloud Run Jobs API → Cloud Run Job → Docker Container → Python Backup Script → Cloud Storage → Cloud Logging

Recovery workflow:

Cloud Storage Object Versioning → Object Generation ID → restore.py → Recovered File

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
| Region | us-central1 |
| Zone | us-central1-a |
| Artifact Registry | gcp-backup-repo |
| Docker Image | backup-job:v1 |
| Cloud Run Job | backup-job |
| Cloud Scheduler | daily-backup-trigger |
| Storage Bucket | project-04354dfd-b58a-4510-a66-backup |
| Backup Object | sample.txt |

Replace project-specific values with your own when recreating the project.

## 5. Project Implementation

### Step 1. Configure GCP Project

Set the active project:

```bash
gcloud config set project PROJECT_ID
```

Check the active project:

```bash
gcloud config get-value project
```

Set the default region:

```bash
gcloud config set compute/region us-central1
```

### Step 2. Enable Required APIs

```bash
gcloud services enable storage.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Step 3. Create Cloud Storage Bucket

Create the bucket:

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

### Step 4. Develop Python Backup Script

Install the required Python library:

```bash
pip install google-cloud-storage
```

The backup script performs these operations:

1. Initializes the Cloud Storage client.
2. Connects to the destination bucket.
3. Generates timestamped backup content.
4. Uploads the file to Cloud Storage.
5. Records execution details using Python logging.
6. Handles exceptions during execution.

Run the local backup script:

```bash
python3 backup.py
```

### Step 5. Develop Python Recovery Script

The recovery script downloads an earlier object generation using its generation ID.

List object versions:

```bash
gcloud storage ls --all-versions gs://BUCKET_NAME/sample.txt
```

Use the required generation ID in `restore.py`.

Run:

```bash
python3 restore.py
```

Verify the recovered file:

```bash
ls -l restored_sample.txt
```

### Step 6. Docker Containerization

Create a Dockerfile using Python 3.12-slim.

The Dockerfile:

- Defines the base Python image.
- Sets the application working directory.
- Installs dependencies.
- Copies the backup script.
- Executes the Python application.

Build a local Docker image:

```bash
docker build -t backup-job:v1 .
```

List Docker images:

```bash
docker images
```

### Step 7. Create Artifact Registry Repository

Create a Docker repository:

```bash
gcloud artifacts repositories create gcp-backup-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="GCP automated backup Docker images"
```

Configure Docker authentication:

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```

Tag the image:

```bash
docker tag backup-job:v1 \
  us-central1-docker.pkg.dev/PROJECT_ID/gcp-backup-repo/backup-job:v1
```

Push the image:

```bash
docker push us-central1-docker.pkg.dev/PROJECT_ID/gcp-backup-repo/backup-job:v1
```

List repository images:

```bash
gcloud artifacts docker images list \
  us-central1-docker.pkg.dev/PROJECT_ID/gcp-backup-repo
```

### Step 8. Build Docker Image Using Cloud Build

Cloud Build was used to build and push the container image.

```bash
gcloud builds submit \
  --tag us-central1-docker.pkg.dev/PROJECT_ID/gcp-backup-repo/backup-job:v1
```

Check build history:

```bash
gcloud builds list --limit=10
```

### Step 9. Configure IAM and Service Accounts

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

The backup service account receives permissions to work with objects in the backup bucket.

### Step 10. Create Cloud Run Job

Deploy the container image as a Cloud Run Job:

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

### Step 11. Configure Cloud Scheduler

Cloud Scheduler was configured to trigger the Cloud Run Job using an authenticated HTTP request.

Enable the Scheduler API:

```bash
gcloud services enable cloudscheduler.googleapis.com
```

Create the Scheduler service account:

```bash
gcloud iam service-accounts create scheduler-invoker \
  --display-name="Cloud Scheduler Invoker"
```

Grant Cloud Run invocation permission:

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

The scheduled execution was successfully verified. The temporary Scheduler job was subsequently deleted.

```bash
gcloud scheduler jobs delete daily-backup-trigger \
  --location=us-central1
```

See [CLOUD-SCHEDULER.md](CLOUD-SCHEDULER.md) for the complete Scheduler configuration and workflow.

### Step 12. Cloud Logging

Cloud Run container logs are collected in Cloud Logging.

Check logs:

```bash
gcloud logging read \
  'resource.type="cloud_run_job" AND resource.labels.job_name="backup-job"' \
  --project=PROJECT_ID \
  --limit=20 \
  --freshness=2h
```

Verify messages such as:

```text
Backup started
Backup uploaded successfully
Bucket: BUCKET_NAME
Object: sample.txt
```

Check execution status:

```bash
gcloud run jobs executions list \
  --job=backup-job \
  --region=us-central1
```

## 6. Backup and Recovery Workflow

### Backup workflow

1. Python generates timestamped backup content.
2. Cloud Run Job starts the Docker container.
3. The container executes backup.py.
4. The Python script connects to Cloud Storage.
5. The script uploads sample.txt.
6. Object Versioning preserves previous generations.
7. Cloud Logging records execution details.

### Recovery workflow

1. List all versions of the backup object.
2. Identify the required generation ID.
3. Configure the generation ID in restore.py.
4. Execute the recovery script.
5. Download the selected version.
6. Verify the recovered file.

## 7. Troubleshooting

| Problem | Resolution |
|---|---|
| Authentication failure | Check active gcloud account and credentials |
| Permission denied during upload | Check bucket IAM permissions |
| Cloud Build staging bucket error | Check Cloud Build service account permissions |
| Artifact Registry push failure | Check Artifact Registry Writer permission |
| Cloud Run execution failure | Inspect job execution details and logs |
| Scheduler invocation failure | Check OAuth identity and roles/run.invoker |
| Restore failure | Verify the object generation ID |
| Missing logs | Check Cloud Logging resource type and time range |

## 8. Repository Structure

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
```

## 9. What I Learned

- Creating and configuring GCP resources.
- Working with Cloud Storage buckets and Object Versioning.
- Using Python for cloud storage automation.
- Building Docker images for cloud workloads.
- Building and publishing images using Cloud Build and Artifact Registry.
- Deploying containerized workloads using Cloud Run Jobs.
- Configuring dedicated service accounts and least-privilege IAM permissions.
- Connecting Cloud Scheduler with the Cloud Run Jobs API.
- Troubleshooting IAM permission errors during Cloud Build and deployment.
- Recovering previous object generations using Python.
- Monitoring container execution through Cloud Logging.

## 10. Project Outcome

Built and tested a containerized Python backup and recovery application on Google Cloud Platform.

Successfully verified:
- Python backup uploads to Cloud Storage.
- Cloud Storage Object Versioning.
- Recovery using object generation IDs.
- Docker image creation and publishing.
- Cloud Run Job execution.
- Cloud Scheduler triggering.
- IAM-based service account permissions.
- Centralized execution logs through Cloud Logging.

Cloud Scheduler was removed after successful testing. The project source code and configuration documentation are retained in GitHub.

## Author

GitHub: https://github.com/nishchiashok14
