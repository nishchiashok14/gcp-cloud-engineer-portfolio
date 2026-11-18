
# GCP Secure VM Management and CI Pipeline

## 1. Project Overview

This project demonstrates secure Linux virtual machine management on Google Cloud Platform (GCP), Python-based VM inventory automation, and Continuous Integration (CI) using GitHub Actions.

The project focuses on:
- Creating and managing Linux virtual machines.
- Securing VM access using SSH and firewall rules.
- Managing permissions using IAM and service accounts.
- Automating VM inventory collection using Python.
- Running automated tests using GitHub Actions.

## 2. Architecture
<img width="1752" height="897" alt="GCP Secure VM CI Architecture" src="https://github.com/user-attachments/assets/c7a2eb3f-9db2-4620-a6ca-a92ff00a7c5d" />

 <img width="313" height="865" alt="image" src="https://github.com/user-attachments/assets/d633943a-69fa-401d-a88c-9b7cec1e0e41" />


## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Google Cloud Platform | Cloud infrastructure |
| Compute Engine | Virtual machine management |
| Ubuntu Linux | VM operating system |
| Python | VM inventory automation |
| Google Cloud Compute Python Client | Communicate with Compute Engine API |
| IAM | Access and permission management |
| VPC Firewall Rules | Control network traffic |
| SSH | Secure remote VM access |
| Git | Version control |
| GitHub | Source code repository |
| GitHub Actions | CI automation |
| Pytest | Automated Python testing |

## 4. GCP Infrastructure Configuration

### VM Configuration

Created a Linux virtual machine using Google Compute Engine.

| Configuration | Value |
|---|---|
| VM Name | project2-linux-vm |
| Machine Type | e2-micro |
| Operating System | Ubuntu 24.04 |
| Zone | asia-south1-a |
| Internal IP | 10.160.0.2 |

### Check VM Status

```bash
gcloud compute instances list
```

### Connect to VM Using SSH

```bash
gcloud compute ssh project2-linux-vm --zone=asia-south1-a
```

### Check VM Details

```bash
gcloud compute instances describe project2-linux-vm --zone=asia-south1-a
```

## 5. Network Security Configuration

Configured VPC firewall rules to restrict SSH access.

Implemented:
- Restricted SSH access to an authorized source IP address.
- Configured TCP port 22 for SSH connectivity.
- Attached a network tag to the VM.
- Associated the firewall rule with the VM using its network tag.
- Disabled the unrestricted default SSH firewall rule.

### Check Firewall Rules

```bash
gcloud compute firewall-rules list
```

### Check VM Network Tags

```bash
gcloud compute instances describe project2-linux-vm \
  --zone=asia-south1-a \
  --format="get(tags.items)"
```

## 6. IAM and Service Account Configuration

Configured IAM permissions for the VM service account.

Roles configured:
- Compute Viewer
- Logs Writer

Configured the Cloud Platform OAuth access scope to allow authenticated Google Cloud API access from the VM.

IAM controls the permissions assigned to the service account, while access scopes control the API access available to applications running on the VM.

## 7. Python VM Inventory Automation

Developed a Python script named `list_vms.py` using the Google Cloud Compute Python Client.

The script communicates with the Compute Engine API and retrieves VM inventory information.

### Information Retrieved

- VM Name
- Machine Type
- VM Status
- Internal IP Address

### Python Library

```python
from google.cloud import compute_v1
```

### Run the Python Script

```bash
python list_vms.py
```

### Sample Output

```text
VM Name: project2-linux-vm
Machine Type: e2-micro
Status: RUNNING
Internal IP: 10.160.0.2
```

Google Cloud authentication and appropriate Compute Engine permissions are required.

## 8. Automated Testing Using Pytest

Created automated unit tests to validate the Python VM inventory function.

Implemented:
- Pytest for automated testing.
- Mocking to simulate Compute Engine API responses.
- Unit testing without requiring a live Compute Engine API call.

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Run Tests

```bash
python -m pytest -v
```

### Test Result

```text
tests/test_list_vms.py::test_list_vms PASSED

1 passed
```

## 9. GitHub Actions CI Pipeline

Implemented a Continuous Integration pipeline using GitHub Actions.

The workflow is triggered when:
- Code is pushed to the main branch.
- A pull request targets the main branch.

### CI Workflow

1. GitHub receives the code push.
2. GitHub Actions starts the workflow.
3. Checks out the repository.
4. Sets up Python 3.12.
5. Installs project dependencies.
6. Runs automated tests using Pytest.
7. Displays the test results.

### Workflow File

```text
.github/workflows/python-ci.yml
```

### CI Pipeline Result

Successfully executed the GitHub Actions workflow.

- Workflow: Python VM Automation CI
- Job: test
- Result: Success
- Automated test: Passed

Note: This project implements Continuous Integration (CI). It does not currently implement Continuous Deployment (CD).

## 10. Project Structure

<img width="500" height="559" alt="image" src="https://github.com/user-attachments/assets/26570c4a-bc32-448a-8269-90b8849399dd" />


## 11. Run the Project Locally

Navigate to the project directory:

```bash
cd 02-vm-automation
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run automated tests:

```bash
python -m pytest -v
```

Run VM inventory automation:

```bash
python python/list_vms.py
```

Ensure Google Cloud authentication and appropriate permissions are configured before running the inventory script.

## 12. Learning Outcomes

- Google Cloud Compute Engine VM management.
- Linux administration and SSH connectivity.
- VPC firewall configuration and network security.
- IAM roles and service account permissions.
- Google Cloud API integration using Python.
- Python automation for cloud resource inventory.
- Unit testing using Pytest and mocking.
- Version control using Git and GitHub.
- Continuous Integration using GitHub Actions.

## 13. Project Conclusion

Built a GCP-based VM management and automation project that combines cloud infrastructure, security configuration, Python scripting, automated testing, and GitHub Actions CI.

The project demonstrates practical exposure to core Cloud Engineer responsibilities, including VM management, access control, cloud API integration, and CI automation.
