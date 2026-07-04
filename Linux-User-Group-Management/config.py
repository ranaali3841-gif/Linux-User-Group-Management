"""Configuration engine for the Linux User & Group Management System."""

import os
from pathlib import Path

# Base Directory Setup
BASE_DIR = Path(__file__).resolve().parent

# Application Settings
APP_NAME = "LinuxUserManager"
VERSION = "1.0.0"

# Directories
LOG_DIR = BASE_DIR / "logs"
BACKUP_DIR = BASE_DIR / "backups"
EXPORT_DIR = BASE_DIR / "exports"
EXPORT_CSV_DIR = EXPORT_DIR / "csv"
EXPORT_JSON_DIR = EXPORT_DIR / "json"

# History Configuration
HISTORY_FILE = LOG_DIR / "cmd_history.json"

# Initialization
for directory in [LOG_DIR, BACKUP_DIR, EXPORT_DIR, EXPORT_CSV_DIR, EXPORT_JSON_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# File Targets
SYSTEM_PASSWD = "/etc/passwd"
SYSTEM_GROUP = "/etc/group"
SYSTEM_SHADOW = "/etc/shadow"