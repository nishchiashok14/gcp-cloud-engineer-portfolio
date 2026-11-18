
# GCP Automated Backup and Recovery System

## 1. Project Overview

This project implements a Python-based backup and recovery system using Google Cloud Storage.

It uploads files to a GCP bucket, preserves previous file versions through Object Versioning, and restores an older version when required.

## 2. Architecture

Local File
    |
    |
    v
Python Backup Script
    |
    |
    v
Google Cloud Storage Bucket
    |
    |
    v
Object Versioning
    |
    |
    v
Python Restore Script
    |
    |
    v
Recovered Local File

## 3. Technologies Used

- Google Cloud Platform
- Google Cloud Storage
- Python
- Google Cloud Storage Python Client
- Google Cloud IAM
- Git and GitHub
- Cloud Shell

## 4. Features

- Automated file upload using Python.
- Cloud Storage Object Versioning.
- Recovery of previous file generations.
- Logging of backup operations.
- Google Cloud authentication through Application Default Credentials.

## 5. GCP Configuration

- Region: us-central1
- Storage Class: Standard
- Uniform Bucket-Level Access: Enabled
- Public Access Prevention: Enforced
- Object Versioning: Enabled

## 6. Project Files

- backup.py: Uploads files to Cloud Storage.
- restore.py: Downloads a selected file generation.
- requirements.txt: Python dependencies.
- backup.log: Backup execution logs.

## 7. Installation

Install the dependencies:

    pip install -r requirements.txt

Authenticate with Google Cloud using an environment with Application Default Credentials configured.

Update the bucket name in backup.py and restore.py.

## 8. Run the Backup

    python3 backup.py

## 9. Restore a Previous Version

Set the required object generation ID in restore.py.

Run:

    python3 restore.py

## 10. Learning Outcomes

- Understanding Google Cloud Storage.
- Working with object generations and versioning.
- Automating cloud operations using Python.
- Using Google Cloud authentication.
- Implementing backup and recovery workflows.
- Tracking operations using Python logging.
