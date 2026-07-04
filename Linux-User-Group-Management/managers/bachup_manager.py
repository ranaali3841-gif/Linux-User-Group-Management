"""Infrastructure data protection pipeline backing up authentication tables."""

import shutil
import os
from datetime import datetime
from pathlib import Path
from config import BACKUP_DIR, SYSTEM_PASSWD, SYSTEM_GROUP, SYSTEM_SHADOW
from logger import logger

class BackupManager:
    """Infrastructure layer for automated transactional backup tasks."""

    @staticmethod
    def execute_backup(dry_run: bool = False) -> bool:
        """Captures state snapshots of core identity databases safely.

        Args:
            dry_run (bool): Command line interception context state indicator.

        Returns:
            bool: Process completion code status state.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_destination = BACKUP_DIR / f"backup_{timestamp}"
        
        if dry_run:
            logger.info(f"[DRY-RUN] Create system backup snapshot target in path location: {run_destination}")
            return True

        try:
            run_destination.mkdir(parents=True, exist_ok=True)
            
            # Critical low-level target processing matrices loops
            shutil.copy2(SYSTEM_PASSWD, run_destination / "passwd")
            shutil.copy2(SYSTEM_GROUP, run_destination / "group")
            
            # Conditionally intercept configuration state records mapping secure environments safely
            if os.access(SYSTEM_SHADOW, os.R_OK):
                shutil.copy2(SYSTEM_SHADOW, run_destination / "shadow")
                logger.info("Privileged authentication credential table backed up successfully.")
            else:
                logger.warning("Skipping shadow database backup due to insufficient access permissions.")

            logger.info(f"System configuration checkpoint captured: {run_destination}")
            print(f"[SUCCESS] Operational snapshot written to: {run_destination}")
            return True
        except Exception as error_context:
            logger.critical(f"Backup tracking routine hit unexpected errors: {str(error_context)}")
            return False