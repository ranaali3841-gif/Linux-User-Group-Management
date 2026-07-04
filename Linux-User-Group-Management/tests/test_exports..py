"""Testing interface targeting output data extraction report pipelines module formats."""

import unittest
from unittest.mock import patch, mock_open
from managers.export_manager import ExportManager

class TestExportReportingPipelines(unittest.TestCase):
    """Validates translation operations structural formats serialization tasks logs summaries."""

    @patch('managers.user_manager.UserManager.list_all_users')
    @patch('managers.group_manager.GroupManager.list_groups')
    @patch('builtins.open', new_callable=mock_open)
    def test_export_data_pipeline_execution(self, mock_file, mock_groups, mock_users):
        """Ensures parsing engines successfully map system state schemas to target report formats."""
        mock_users.return_value = [{"username": "adm", "uid": "1000", "gid": "1000", "gecos": "", "home": "/home/adm", "shell": "/bin/bash"}]
        mock_groups.return_value = [{"group_name": "adm", "gid": "1000", "members": "adm"}]
        
        status = ExportManager.export_data()
        self.assertTrue(status)
        self.assertTrue(mock_file.called)