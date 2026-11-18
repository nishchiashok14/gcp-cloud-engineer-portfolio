# GCP Automated Backup and Recovery System

## Project Overview

This project demonstrates an automated backup and recovery system built using Google Cloud Platform (GCP).

It uses Google Cloud Storage to store backup files, Cloud Run Jobs to execute Python backup scripts, Docker to package the application, and Cloud Scheduler to trigger backups automatically.

## Architecture

Cloud Scheduler -> Cloud Run Job -> Docker Container -> Python Backup Script -> Google Cloud Storage -> Cloud Logging
<img width="1752" height="897" alt="GCP Automated Backup Recovery Architecture" src="https://github.com/user-attachments/assets/74fda5cd-4aa2-4150-a560-1c1ebf1a0bdb" />

## Technologies Used

- Google Cloud Platform (GCP)
- Google Cloud Storage
- Cloud Run Jobs
- Cloud Scheduler
- Artifact Registry
- Cloud Build
- Docker
- Python
- IAM
- Cloud Logging
- Git and GitHub

## Project Implementation

### 1. Cloud Storage Setup

- Created a Cloud Storage bucket.
- Configured the bucket in `us-central1`.
- Enabled Object Versioning.
- Configured uniform bucket-level access.
- Enabled public access prevention.

### 2. Python Backup Script

Developed a Python script using the Google Cloud Storage client library.

The script:
- Generates timestamped backup content.
- Connects to Cloud Storage.
- Uploads the backup file.
- Records backup activity using Python logging.

### 3. Docker Containerization

- Created a Dockerfile.
- Used Python 3.12 as the base image.
- Installed required Python dependencies.
- Packaged the backup application into a Docker image.

### 4. Cloud Build and Artifact Registry

- Used Cloud Build to build the Docker image.
- Created an Artifact Registry repository.
- Stored the Docker image in Artifact Registry.

Image: `backup-job:v1`

### 5. Cloud Run Job

- Created a Cloud Run Job.
- Configured a dedicated service account.
- Assigned Cloud Storage permissions.
- Executed the backup container.
- Verified successful backup execution.

### 6. Cloud Scheduler

- Created a Cloud Scheduler HTTP job.
- Configured OAuth authentication.
- Connected Cloud Scheduler to the Cloud Run Jobs API.
- Configured a scheduled backup trigger.

### 7. Logging and Monitoring

- Configured Python logging.
- Used Cloud Logging to inspect execution logs.
- Verified backup execution status.

### 8. Backup Recovery

- Enabled Cloud Storage Object Versioning.
- Created a Python restoration script.
- Used object generations to identify previous file versions.

## Project Features

- Automated backup execution
- Docker-based application deployment
- Cloud Storage object versioning
- Scheduled backup triggering
- IAM-based access control
- Backup execution logging
- File recovery support

## Repository Structure

```text
01-backup-recovery/
│
├── backup.py
├── restore.py
├── requirements.txt
├── Dockerfile
├── README.md
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
    └── 11-cloud-logging.png
```

## What I Learned

- Creating and configuring GCP resources.
- Working with Cloud Storage.
- Writing Python automation scripts.
- Building Docker images.
- Using Cloud Build and Artifact Registry.
- Deploying and executing Cloud Run Jobs.
- Configuring Cloud Scheduler.
- Managing IAM permissions.
- Monitoring cloud workloads using Cloud Logging.

## Project Outcome

Built a containerized Python backup application on Google Cloud Platform, executed it through Cloud Run Jobs, stored backup files in Cloud Storage, and configured Cloud Scheduler for automated execution.

## Author

GitHub: https://github.com/nishchiashok14
