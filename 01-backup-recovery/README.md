# GCP Automated Backup and Recovery System

## Project Overview

A Python-based backup and recovery system built on Google Cloud Platform (GCP).

The project uses Cloud Storage for backup storage, Python for backup and recovery, Docker for containerization, Cloud Build for image creation, Artifact Registry for image storage, and Cloud Run Jobs for execution.

Cloud Scheduler was tested as the automated trigger.

## Architecture

![GCP Automated Backup Recovery Architecture](https://github.com/user-attachments/assets/74fda5cd-4aa2-4150-a560-1c1ebf1a0bdb)

Cloud Scheduler → Cloud Run Jobs API → Cloud Run Job → Docker Container → Python Backup Script → Cloud Storage → Cloud Logging

## Technologies Used

- Google Cloud Platform
- Cloud Storage
- Cloud Run Jobs
- Cloud Scheduler
- Artifact Registry
- Cloud Build
- Docker
- Python 3.12
- IAM
- Cloud Logging
- Git and GitHub

## Project Implementation

### 1. Cloud Storage

- Created a bucket in `us-central1`.
- Enabled Object Versioning.
- Configured uniform bucket-level access.
- Enabled public access prevention.
- Configured backup object storage.

### 2. Python Backup Script

- Used the Google Cloud Storage Python client library.
- Generated timestamped backup content.
- Uploaded backup objects to Cloud Storage.
- Added Python logging for execution tracking.
- Implemented exception handling.

### 3. Docker Containerization

- Created a Dockerfile.
- Used Python 3.12-slim as the base image.
- Installed dependencies using `requirements.txt`.
- Packaged the backup script into a Docker image.

### 4. Cloud Build and Artifact Registry

- Built the Docker image using Cloud Build.
- Created an Artifact Registry Docker repository.
- Stored the image as `backup-job:v1`.

### 5. Cloud Run Jobs

- Created a Cloud Run Job named `backup-job`.
- Configured a dedicated service account.
- Granted Cloud Storage object permissions.
- Executed the container successfully.
- Verified backup uploads.

### 6. Cloud Scheduler

- Created an HTTP Scheduler job.
- Configured OAuth authentication.
- Used a dedicated Scheduler service account.
- Connected Scheduler to the Cloud Run Jobs API.
- Tested the scheduled execution successfully.
- Deleted the temporary Scheduler after testing.

See [CLOUD-SCHEDULER.md](CLOUD-SCHEDULER.md) for configuration commands and workflow.

### 7. Cloud Logging

- Used Python logging.
- Inspected execution logs in Cloud Logging.
- Verified backup start and successful upload messages.
- Checked container exit status.

### 8. Backup Recovery

- Enabled Object Versioning.
- Identified object generations.
- Used `restore.py` to download an earlier object generation.
- Verified file recovery.

## How to Run

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the local backup script

```bash
python3 backup.py
```

### Run the restore script

```bash
python3 restore.py
```

### List object versions

```bash
gcloud storage ls --all-versions gs://BUCKET_NAME/sample.txt
```

### Execute the Cloud Run Job

```bash
gcloud run jobs execute backup-job --region=us-central1 --wait
```

Replace `BUCKET_NAME` with your bucket name. Configure GCP authentication and IAM permissions before running the scripts.

## Troubleshooting

| Issue | Troubleshooting |
|---|---|
| Permission denied during upload | Check the backup service account's bucket IAM permissions |
| Cloud Run Job fails | Inspect execution status and Cloud Logging |
| Scheduler cannot invoke Cloud Run | Check `roles/run.invoker` |
| Restore fails | Verify the object generation ID |
| Docker build fails | Check Dockerfile, dependencies and Cloud Build permissions |

## Repository Structure

```text
01-backup-recovery/
├── backup.py
├── restore.py
├── requirements.txt
├── Dockerfile
├── README.md
├── CLOUD-SCHEDULER.md
├── docs/
│   ├── architecture-automated.png
│   └── architecture-recovery.png
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

## What I Learned

- Configuring Cloud Storage Object Versioning and recovering earlier object generations.
- Building Docker images with Cloud Build.
- Storing and managing container images in Artifact Registry.
- Executing containerized Python workloads using Cloud Run Jobs.
- Configuring IAM permissions for separate service accounts.
- Connecting Cloud Scheduler to the Cloud Run Jobs API.
- Troubleshooting Cloud Build permissions and Cloud Run execution.
- Monitoring backup operations through Cloud Logging.
- Understanding how object generations support recovery.

## Project Outcome

Built and tested a containerized Python backup application using GCP services. Verified backup execution, Cloud Storage uploads, object versioning, recovery, scheduled triggering and centralized logging.

## Author

GitHub: https://github.com/nishchiashok14
