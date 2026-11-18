# GCP Secure VM Management and CI Pipeline

Secure Linux VM management on Google Cloud Platform (GCP), Python-based VM inventory automation, and automated testing with GitHub Actions.

## 1. Project Overview

This project shows how to create and secure a Linux virtual machine on Compute Engine, give it least-privilege access using IAM, automate VM inventory with Python, and test the code automatically with a CI pipeline.

Key goals:

- Create and manage a Linux VM on Compute Engine.
- Secure SSH access using a restricted firewall rule.
- Manage permissions with IAM and a service account.
- Automate VM inventory collection with Python.
- Run automated tests on every push using GitHub Actions.

## 2. Architecture
<img width="1752" height="897" alt="GCP Secure VM CI Architecture" src="https://github.com/user-attachments/assets/c7a2eb3f-9db2-4620-a6ca-a92ff00a7c5d" />

<img width="653" height="323" alt="image" src="https://github.com/user-attachments/assets/761d8ddb-7567-46d5-89a4-8a563e78121b" />


## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Google Cloud Platform | Cloud infrastructure |
| Compute Engine | Virtual machine management |
| Ubuntu Linux 24.04 LTS | VM operating system |
| Python 3 and venv | VM inventory automation |
| google-cloud-compute | Python client for the Compute Engine API |
| IAM and service accounts | Access and permission management |
| VPC firewall rules and network tags | Control network traffic |
| SSH | Secure remote VM access |
| Git and GitHub | Version control and code hosting |
| GitHub Actions | Continuous Integration |
| Pytest and unittest.mock | Automated testing |

## 4. GCP Infrastructure

### VM configuration

| Setting | Value |
|---|---|
| VM name | project2-linux-vm |
| Machine type | e2-micro |
| Operating system | Ubuntu 24.04 LTS |
| Zone | asia-south1-a (Mumbai) |
| Internal IP | 10.160.0.2 |

### Key commands

Enable the Compute Engine API:

```bash
gcloud services enable compute.googleapis.com
```

Create the VM:

```bash
gcloud compute instances create project2-linux-vm \
  --zone=asia-south1-a \
  --machine-type=e2-micro \
  --image-family=ubuntu-2404-lts-amd64 \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=10GB
```

Check VM status:

```bash
gcloud compute instances list
```

Connect over SSH:

```bash
gcloud compute ssh project2-linux-vm --zone=asia-south1-a
```

## 5. Network Security

The default `default-allow-ssh` rule allowed SSH from `0.0.0.0/0` (the whole internet). I replaced it with a restricted rule:

- Created a new firewall rule allowing TCP port 22 only from a single IP address (`/32`).
- Attached a network tag to the VM.
- Applied the rule to the VM through that network tag.
- Disabled the unrestricted default SSH rule.

```bash
gcloud compute firewall-rules create project2-allow-ssh \
  --network=default \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:22 \
  --source-ranges=<YOUR_IP>/32 \
  --target-tags=project2-vm

gcloud compute instances add-tags project2-linux-vm \
  --zone=asia-south1-a \
  --tags=project2-vm

gcloud compute firewall-rules update default-allow-ssh --disabled
```

Verify:

```bash
gcloud compute firewall-rules list
gcloud compute firewall-rules describe default-allow-ssh --format="get(disabled)"
gcloud compute instances describe project2-linux-vm \
  --zone=asia-south1-a \
  --format="get(tags.items)"
```

## 6. IAM and Service Account

The VM runs with a service account that has only the permissions it needs:

| Role | Why |
|---|---|
| Compute Viewer | Read-only access to list VMs (the script only reads) |
| Logs Writer | Lets the VM write logs to Cloud Logging |

The Cloud Platform OAuth access scope is configured so applications on the VM can call Google Cloud APIs.

IAM controls what the service account is allowed to do. Access scopes limit which APIs the VM's credentials can reach. Both must allow an action for it to work.

No keys or passwords are stored in the code. The script authenticates through the VM's service account using Application Default Credentials.

## 7. Python VM Inventory Automation

`python/list_vms.py` uses the Google Cloud Compute Python client to read VM information from the Compute Engine API.

It retrieves:

- VM name
- Machine type
- VM status
- Internal IP address

```python
from google.cloud import compute_v1
```

Sample output:

```text
VM Name: project2-linux-vm
Machine Type: e2-micro
Status: RUNNING
Internal IP: 10.160.0.2
```

The script was developed and run on the VM inside a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install google-cloud-compute
python list_vms.py
```

Google Cloud authentication and Compute Engine read permission are required.

## 8. Automated Testing with Pytest

Unit tests validate the VM inventory function.

- Pytest runs the tests.
- Mocking simulates Compute Engine API responses, so no live API call, credentials, or cost are needed.
- The same tests run locally and in CI.

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

Result:

```text
tests/test_list_vms.py::test_list_vms PASSED

1 passed
```

## 9. GitHub Actions CI Pipeline

The workflow runs when code is pushed to `main` or a pull request targets `main`.

Pipeline steps:

1. GitHub receives the push.
2. GitHub Actions starts a fresh Ubuntu runner.
3. The repository is checked out.
4. Python 3.12 is set up.
5. Dependencies are installed from `requirements.txt`.
6. Pytest runs inside `02-vm-automation`.
7. Results show as a green tick (pass) or red cross (fail).

Workflow file (must be at the repository root):

```text
.github/workflows/python-ci.yml
```

Latest result: workflow succeeded, test job passed.

Note: this project implements Continuous Integration (CI). It does not implement Continuous Deployment (CD).

## 10. Project Structure

<img width="327" height="340" alt="image" src="https://github.com/user-attachments/assets/85b69346-9a5d-42a5-8f35-62c4b54a7093" />


## 11. Run Locally

```bash
cd 02-vm-automation
python -m pip install -r requirements.txt
python -m pytest -v
python python/list_vms.py
```

The inventory script needs Google Cloud authentication and Compute Engine read permission. The tests do not.

## 12. Challenges and Fixes

| Problem | Cause | Fix |
|---|---|---|
| `pytest: command not found` | Installed in `~/.local/bin`, which is not on PATH | Run `python3 -m pytest` |
| CI could not find the `python` package | Tests ran from the repo root | Added `working-directory: 02-vm-automation` to the test step |
| Workflow did not run from subfolder | GitHub only reads `.github/workflows` at the repo root | Removed the duplicate and kept the root workflow |
| SSH open to the whole internet | Default rule allowed `0.0.0.0/0` | Created a `/32` rule and disabled the default |
| Cache files in the repo | `__pycache__` and `.pytest_cache` were generated | Removed them and ignored them in `.gitignore` |

## 13. Learning Outcomes

- Compute Engine VM creation and management
- Linux administration and SSH connectivity
- VPC firewall configuration and network tags
- IAM roles, service accounts, and least privilege
- Google Cloud API integration with Python
- Python virtual environments and dependency management
- Unit testing with Pytest and mocking
- Version control with Git and GitHub
- Continuous Integration with GitHub Actions

## 14. Project Conclusion

Built a GCP-based VM management and automation project that combines cloud infrastructure, security configuration, Python scripting, automated testing, and GitHub Actions CI.

The project demonstrates practical exposure to core Cloud Engineer responsibilities, including VM management, access control, cloud API integration, and CI automation.
