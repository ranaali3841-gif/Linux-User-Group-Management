"""Low-level execution abstraction tracking user authentication and access locks."""

import chardet
from utils.helpers import execute_command
from utils.validator import InputValidator
from logger import logger

class PasswordManager:
    """Security interface managing platform user security constraints and authorization attributes."""

    @staticmethod
    def change_password(username: str, password: str, dry_run: bool = False) -> bool:
        """Safely updates target user structural authentication credential targets.

        Args:
            username (str): Evaluation targeted username target.
            password (str): Secure clear text replacement value string.
            dry_run (bool): State execution flag bypass indicator.

        Returns:
            bool: Operation status flag.
        """
        if not InputValidator.validate_username(username):
            logger.error(f"Password modification failure. Invalid structural account name: {username}")
            return False

        if dry_run:
            logger.info(f"[DRY-RUN] Update password mapping for user account context: {username}")
            return True

        # Pipeline standard stream input components safely avoiding dynamic evaluation logic
        try:
            import subprocess
            cmd = ["chpasswd"]
            logger.info(f"Targeting password pipeline update structure for: {username}")
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input=f"{username}:{password}")
            
            if process.returncode == 0:
                logger.info(f"Password context successfully mapped to account: {username}")
                return True
            logger.error(f"Credential injection error: {stderr.strip()}")
            return False
        except Exception as err:
            logger.error(f"Catastrophic failure within credential update stack: {str(err)}")
            return False

    @staticmethod
    def lock_account(username: str, dry_run: bool = False) -> bool:
        """Locks target system account, preventing standard active user sessions."""
        if not InputValidator.validate_username(username):
            return False
        status, _, stderr = execute_command(["usermod", "-L", username], dry_run)
        if status:
            logger.info(f"User account security scope locked successfully: {username}")
        return status

    @staticmethod
    def unlock_account(username: str, dry_run: bool = False) -> bool:
        """Unlocks locked user identity mappings."""
        if not InputValidator.validate_username(username):
            return False
        status, _, stderr = execute_command(["usermod", "-U", username], dry_run)
        if status:
            logger.info(f"User account access context restored: {username}")
        return status

    @staticmethod
    def force_password_reset(username: str, dry_run: bool = False) -> bool:
        """Forces immediate update rules demanding renewal upon subsequent entry interaction loops."""
        if not InputValidator.validate_username(username):
            return False
        status, _, stderr = execute_command(["chage", "-d", "0", username], dry_run)
        if status:
            logger.info(f"Password updates marked mandatory for user context: {username}")
        return status