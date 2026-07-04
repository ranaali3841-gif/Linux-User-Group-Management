"""Validation execution test suite maps parsing user interactions management routines logic."""

import unittest
from unittest.mock import patch
from utils.validator import InputValidator
from managers.user_manager import UserManager

class TestUserExecutionInfrastructure(unittest.TestCase):
    """Verifies interface code interactions patterns parsing user configuration elements structural steps."""

    def test_username_regex_validation_rules(self):
        """Ensures validation boundaries isolate and block shell character injection sequences."""
        self.assertTrue(InputValidator.validate_username("devops_user"))
        self.assertTrue(InputValidator.validate_username("alpha-numeric9"))
        self.assertFalse(InputValidator.validate_username("bad;user"))
        self.assertFalse(InputValidator.validate_username("invalid user"))
        self.assertFalse(InputValidator.validate_username("root;rm -rf /"))

    @patch('utils.helpers.execute_command')
    def test_create_user_dry_run_routing(self, mock_execution_pipeline):
        """Verifies programmatic construction workflows pass configuration parameters through dry run mode flags accurately."""
        mock_execution_pipeline.return_value = (True, "DRY_RUN_SUCCESS", "")
        outcome = UserManager.create_user("testadmin", shell="/bin/bash", dry_run=True)
        self.assertTrue(outcome)
        mock_execution_pipeline.assert_called_once_with(["useradd", "-m", "-s", "/bin/bash", "testadmin"], True)