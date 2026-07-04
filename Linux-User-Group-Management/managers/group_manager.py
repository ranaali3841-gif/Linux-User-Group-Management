"""Low-level management layer wrapping identity structures tracking group parameters."""

import grp
from typing import List, Dict, Optional
from utils.helpers import execute_command
from utils.validator import InputValidator
from logger import logger

class GroupManager:
    """Core administrative interface for local group policy management."""

    @staticmethod
    def create_group(group_name: str, dry_run: bool = False) -> bool:
        """Generates configuration sets injecting isolated identity parameters."""
        if not InputValidator.validate_group_name(group_name):
            logger.error(f"Group identity pattern constraints verification dropped for: {group_name}")
            return False
        status, _, _ = execute_command(["groupadd", group_name], dry_run)
        return status

    @staticmethod
    def delete_group(group_name: str, dry_run: bool = False) -> bool:
        """Removes local group access mappings securely."""
        if not InputValidator.validate_group_name(group_name):
            return False
        status, _, _ = execute_command(["groupdel", group_name], dry_run)
        return status

    @staticmethod
    def rename_group(old_name: str, new_name: str, dry_run: bool = False) -> bool:
        """Renames an existing local identity block mapping name targets."""
        if not InputValidator.validate_group_name(old_name) or not InputValidator.validate_group_name(new_name):
            return False
        status, _, _ = execute_command(["groupmod", "-n", new_name, old_name], dry_run)
        return status

    @staticmethod
    def add_user_to_group(username: str, group_name: str, dry_run: bool = False) -> bool:
        """Appends supplementary group permissions flags to target user accounts."""
        if not InputValidator.validate_username(username) or not InputValidator.validate_group_name(group_name):
            return False
        status, _, _ = execute_command(["usermod", "-aG", group_name, username], dry_run)
        return status

    @staticmethod
    def remove_user_from_group(username: str, group_name: str, dry_run: bool = False) -> bool:
        """Removes an active local user from a supplementary group specification."""
        if not InputValidator.validate_username(username) or not InputValidator.validate_group_name(group_name):
            return False
        status, _, _ = execute_command(["gpasswd", "-d", username, group_name], dry_run)
        return status

    @staticmethod
    def list_groups() -> List[Dict[str, str]]:
        """Parses operational configuration structures mapped down inside storage entries."""
        groups = []
        for g in grp.getgrall():
            if g.gr_gid >= 1000 or g.gr_name == "root":
                groups.append({
                    "group_name": g.gr_name,
                    "gid": str(g.gr_gid),
                    "members": ",".join(g.gr_mem)
                })
        return groups

    @staticmethod
    def get_group_info(group_name: str) -> Optional[Dict[str, str]]:
        """Resolves internal structures isolating targets by identity names."""
        try:
            res = grp.getgrnam(group_name)
            return {
                "group_name": res.gr_name,
                "gid": str(res.gr_gid),
                "members": ",".join(res.gr_mem)
            }
        except KeyError:
            return None