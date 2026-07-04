"""Telemetry reporting pipeline exporting user structures to standardized formats."""

import csv
import json
from config import EXPORT_CSV_DIR, EXPORT_JSON_DIR
from managers.user_manager import UserManager
from managers.group_manager import GroupManager
from logger import logger

class ExportManager:
    """Data orchestration engine exporting local system user and group metrics."""

    @staticmethod
    def export_data() -> bool:
        """Transforms active system state metrics into clean, structured external logs.

        Returns:
            bool: Status of the export process.
        """
        try:
            users = UserManager.list_all_users()
            groups = GroupManager.list_groups()

            # Export active user base metadata targets into CSV structures
            csv_user_path = EXPORT_CSV_DIR / "users_summary.csv"
            with open(csv_user_path, mode="w", newline="", encoding="utf-8") as out_csv:
                writer = csv.DictWriter(out_csv, fieldnames=["username", "uid", "gid", "gecos", "home", "shell"])
                writer.writeheader()
                writer.writerows(users)

            # Export group specifications to structural configuration arrays
            json_dump_path = EXPORT_JSON_DIR / "system_matrix.json"
            combined_payload = {
                "extracted_users": users,
                "extracted_groups": groups
            }
            with open(json_dump_path, mode="w", encoding="utf-8") as out_json:
                json.dump(combined_payload, out_json, indent=4)

            logger.info("Local configuration matrices exported successfully.")
            print(f"[SUCCESS] Structured tables extracted.\n-> CSV: {csv_user_path}\n-> JSON: {json_dump_path}")
            return True
        except Exception as exc:
            logger.error(f"Pipeline mapping processing generated fatal context errors: {str(exc)}")
            return False