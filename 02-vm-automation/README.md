# GCP Secure VM Management and CI Pipeline

## Project Overview

This project demonstrates secure Linux VM management on Google Cloud Platform (GCP), Python-based VM inventory automation, and automated testing using GitHub Actions.

## Technologies Used

- Google Cloud Platform
- Compute Engine
- Ubuntu Linux
- Python
- Google Cloud Compute Python Client
- IAM
- VPC Firewall Rules
- Git and GitHub
- GitHub Actions
- Pytest

## Infrastructure Configuration

- Created a Linux VM using GCP Compute Engine.
- Configured SSH access through a restricted firewall rule.
- Attached a network tag to the VM.
- Configured IAM permissions for the VM service account.
- Configured API access scopes.

## Python Automation

Created a Python script to retrieve VM inventory information from Compute Engine.

The script displays:
- VM name
- Machine type
- VM status
- Internal IP address

## Automated Testing and CI

- Created unit tests using Pytest.
- Used mocking to test the VM inventory function without calling the live Compute Engine API.
- Configured GitHub Actions to install dependencies and run tests on pushes to the main branch and pull requests targeting main.

## Project Structure

```text
02-vm-automation/
├── python/
│   ├── __init__.py
│   └── list_vms.py
├── tests/
│   └── test_list_vms.py
├── requirements.txt
└── README.md
```

Workflow location: `.github/workflows/python-ci.yml`

## Run Locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest -v
```

Run VM inventory:

```bash
python python/list_vms.py
```

Google Cloud authentication and appropriate Compute Engine permissions are required to run the inventory script.

## CI Pipeline Result

GitHub Actions successfully executed the automated test job after a push to the main branch.

## Learning Outcomes

- GCP Compute Engine VM management
- Linux administration
- SSH and firewall configuration
- IAM and service accounts
- Python cloud automation
- Pytest unit testing
- GitHub Actions CI automation
