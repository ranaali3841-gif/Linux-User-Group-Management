# Linux User & Group Management System

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security Level](https://img.shields.io/badge/Security-Production--Ready-red.svg)]()

A secure, modular Command Line Interface (CLI) application engineered for Linux Systems Administrators and DevOps Engineers to automate and manage local system user and group lifecycles safely.

## Project Structure

```text
Linux-User-Group-Management/
│
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── main.py
├── config.py
├── logger.py
│
├── managers/
│   ├── __init__.py
│   ├── user_manager.py
│   ├── group_manager.py
│   ├── password_manager.py
│   ├── backup_manager.py
│   └── export_manager.py
│
├── utils/
│   ├── validator.py
│   ├── permissions.py
│   ├── helpers.py
│   └── history.py
│
├── logs/
├── backups/
├── exports/
│   ├── csv/
│   └── json/
│
└── tests/
    ├── test_user.py
    ├── test_group.py
    ├── test_permissions.py
    └── test_exports.py
```

 # Installation & Setup
Clone this project repository into your local production environment:
```
Bash
git clone https://github.com/ranaali3841-gif/Linux-User-Group-Management.git
cd Linux-User-Group-Management
```
Initialize and activate a localized virtual environment for development:
```
Bash
python3 -m venv venv
source venv/bin/activate
```
Install development dependencies:
```
Bash
pip install -r requirements.txt
```

# Production CLI Usage Syntax Guide
[!IMPORTANT]
Administrative actions modifying system authentication tables require root execution context (sudo). Read-only inspection tasks (e.g., list-users, history) can run under non-privileged scopes safely.

 # User Account Management Examples
List Local Users:
```
Bash
python main.py list-users
```
Provision New Standard System User Account:
```
Bash
sudo python main.py create-user username_here --shell /bin/bash
```
Check Specified Target User Configuration Account Details:
```
Bash
python main.py info username_here
```
Lock and Suspend Target Active User Account Sessions:
```
Bash
sudo python main.py lock-user username_here
```
Purge Account Context Mapping Records and Associated Home Directories:
```
Bash
sudo python main.py delete-user username_here
```


# Group Policy Control Subcommands
Provision New Target Group Identity Structure Module Context:
```
Bash
sudo python main.py create-group group_name_here
```
Append User Account Target to Supplementary Group Assignment Metrics:
```
Bash
sudo python main.py add-group username_here group_name_here
```


# Platform Maintenance Task Subcommands
Generate High-Reliability Structural Data Backups:
```
Bash
sudo python main.py backup
```
Export Analytics Matrix Logs Summaries Summarizing State Records Data:
```
Bash
sudo python main.py export
```
Inspect Auditable Execution Action Trace Logs Histories Telemetry:
```
Bash
python main.py history
```


# Dry Run Verification Engine
Append the --dry-run global verification parameter flag anywhere in your pipeline sequence to preview changes without committing actual system mutations:
```
Bash
sudo python main.py --dry-run create-user prospective_user
```
Executing Automated Test Frameworks
Run the integrated automated test suite using pytest:
```
Bash
pytest -v
```

# Security Notes
Uses zero-shell subprocess parameters to block command injection exploits.

Enforces structural regular expression checks on usernames and group definitions.

Standard logs explicitly scrub inputs to prevent password leakage in clean-text diagnostic log archives.

```