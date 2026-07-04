"""Transaction ledger mapping system command line telemetry history."""

import json
from datetime import datetime
from config import HISTORY_FILE

class AuditHistory:
    """History logger for management actions tracking administrative mutations."""

    @staticmethod
    def log_action(command: str, arguments: list, executed_by: str, status: str) -> None:
        """Tracks executing operations into a structured JSON historical catalog.

        Args:
            command (str): Target runtime positional execution block.
            arguments (list): Scrubbed and filtered array payload items.
            executed_by (str): Local contextual username executing current tasking loop.
            status (str): Outcome flag tracking operational states.
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "arguments": [str(arg) for arg in arguments if "pass" not in str(arg).lower()],
            "user": executed_by,
            "status": status
        }
        
        history_data = []
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as file_stream:
                    history_data = json.load(file_stream)
            except json.JSONDecodeError:
                history_data = []

        history_data.append(record)
        
        with open(HISTORY_FILE, "w", encoding="utf-8") as file_stream:
            json.dump(history_data, file_stream, indent=4)

    @staticmethod
    def read_history() -> list:
        """Reads operational application JSON log strings.

        Returns:
            list: Parsed structural objects collection representing executed changes.
        """
        if not HISTORY_FILE.exists():
            return []
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file_stream:
                return json.load(file_stream)
        except json.JSONDecodeError:
            return []