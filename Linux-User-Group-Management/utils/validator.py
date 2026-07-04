"""Deterministic validation engine preventing shell injection attacks."""

import re
from pathlib import Path
from typing import Optional

class InputValidator:
    """Validation schemas for ensuring deterministic Linux identity operations."""

    @staticmethod
    def validate_username(username: str) -> bool:
        """Validates Linux standard standard POSIX user identifier formats.

        Args:
            username (str): Target evaluation string identifier.

        Returns:
            bool: Validation correctness status.
        """
        if not username or len(username) > 32:
            return False
        # Matches lowercase alphanumeric strings matching native system parameters
        return bool(re.match(r'^[a-z_][a-z0-9_-]*\$?$', username))

    @staticmethod
    def validate_group_name(group_name: str) -> bool:
        """Validates compliance parameters for POSIX standard groups.

        Args:
            group_name (str): Intended targeted identity value.

        Returns:
            bool: Validation match state.
        """
        if not group_name or len(group_name) > 32:
            return False
        return bool(re.match(r'^[a-z_][a-z0-9_-]*$', group_name))

    @staticmethod
    def validate_shell(shell_path: str) -> bool:
        """Validates requested login shell exists and contains absolute structural paths.

        Args:
            shell_path (str): Fully qualified target operational path.

        Returns:
            bool: Validation certainty.
        """
        path = Path(shell_path)
        return path.is_absolute() and os.access(path, os.X_OK)