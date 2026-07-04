"""Privilege detection engine ensuring valid root invocation vector fields."""

import os
import sys
from logger import logger

def is_root() -> bool:
    """Evaluates whether execution runtime context possesses POSIX Root privileges.

    Returns:
        bool: True if executing user context is root (UID 0), False otherwise.
    """
    return os.geteuid() == 0

def enforce_root() -> None:
    """Enforces execution barriers stopping logic execution if missing root privileges."""
    if not is_root():
        logger.error("Root privilege verification failed. Operation rejected.")
        print("[CRITICAL ERROR] Administrative privileges required. Re-run execution using sudo.")
        sys.exit(1)