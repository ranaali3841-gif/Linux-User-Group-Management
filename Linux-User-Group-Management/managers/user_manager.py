"""System abstraction layer exposing active management logic workflows for Linux accounts."""

import pwd
import os
from typing import List, Dict, Optional
from utils.helpers import execute_command
from utils.validator import InputValidator
from logger import logger

class UserManager:
    """Core administrative orchestration interface managing local POSIX accounts."""

    @staticmethod
    def create_user(username: str, home_dir: Optional[str] = None, shell: Optional[str] = None, dry_run: bool = False) -> bool:
        """Creates a new local Linux user account securely with explicit arguments."""
        if not InputValidator.validate_username(username):
            logger.error(f"Account validation identity constraints check failed: {username}")
            return False

        cmd = ["useradd", "-m"]
        if home_dir:
            cmd.extend(["-d", home_dir])
        if shell:
            if not InputValidator.validate_shell(shell):
                logger.error(f"Requested shell execution vector is invalid or missing execution targets: {shell}")
                return False
            cmd.extend(["-s", shell])
        cmd.append(username)

        status, _, stderr = execute_command(cmd, dry_run)
        if status:
            logger.info(f"Successfully provisioned structural system account: {username}")
        return status

    @staticmethod
    def delete_user(username: str, remove_home: bool = True, dry_run: bool = False) -> bool:
        """Deletes a local user account and cleans up associated runtime storage tracking artifacts."""
        if not InputValidator.validate_username(username):
            return False

        cmd = ["userdel"]
        if remove_home:
            cmd.append("-r")
        cmd.append(username)

        status, _, stderr = execute_command(cmd, dry_run)
        if status:
            logger.info(f"Account identity purge operation completed for target: {username}")
        return status

    @staticmethod
    def modify_user_login_shell(username: str, new_shell: str, dry_run: bool = False) -> bool:
        """Updates login shell tracking contexts."""
        if not InputValidator.validate_username(username) or not InputValidator.validate_shell(new_shell):
            return False
        status, _, _ = execute_command(["usermod", "-s", new_shell, username], dry_run)
        return status

    @staticmethod
    def change_home_directory(username: str, new_home: str, dry_run: bool = False) -> bool:
        """Relocates user home path maps structural target endpoints dynamically."""
        if not InputValidator.validate_username(username):
            return False
        status, _, _ = execute_command(["usermod", "-m", "-d", new_home, username], dry_run)
        return status

    @staticmethod
    def list_all_users() -> List[Dict[str, str]]:
        """Parses active database metrics tracking contexts out of the standard layout architecture.

        Returns:
            List[Dict[str, str]]: Structural map outputs capturing configuration arrays.
        """
        users = []
        for user_entry in pwd.getpwall():
            # Filter low-range platform system reserved values out of core visual sets cleanly
            if user_entry.pw_uid >= 1000 or user_entry.pw_name == "root":
                users.append({
                    "username": user_entry.pw_name,
                    "uid": str(user_entry.pw_uid),
                    "gid": str(user_entry.pw_gid),
                    "gecos": user_entry.pw_gecos,
                    "home": user_entry.pw_dir,
                    "shell": user_entry.pw_shell
                })
        return users

    @staticmethod
    def search_user(username: str) -> Optional[Dict[str, str]]:
        """Queries localized structured state entries searching for active user matches."""
        try:
            res = pwd.getpwnam(username)
            return {
                "username": res.pw_name,
                "uid": str(res.pw_uid),
                "gid": str(res.pw_gid),
                "gecos": res.pw_gecos,
                "home": res.pw_dir,
                "shell": res.pw_shell
            }
        except KeyError:
            logger.warning(f"Target record lookup array yielded empty results mapping search for: {username}")
            return None