"""Execution execution abstractions mapping internal subprocess pipelines."""

import subprocess
from typing import List, Tuple
from logger import logger

def execute_command(cmd: List[str], dry_run: bool = False) -> Tuple[bool, str, str]:
    """Wraps subprocess pipelines preventing shell-injection vectors safely.

    Args:
        cmd (List[str]): Exploded list containing explicit targets and operational flags.
        dry_run (bool): Evaluation bypass intercept flag.

    Returns:
        Tuple[bool, str, str]: Evaluation status boolean, stdout string, and stderr capture string.
    """
    if dry_run:
        logger.info(f"[DRY-RUN EXECUTION INTERCEPT]: {' '.join(cmd)}")
        return True, "DRY_RUN_SUCCESS", ""

    try:
        logger.info(f"Executing system lifecycle binary vector: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return True, result.stdout.strip(), result.stderr.strip()
        else:
            logger.error(f"Command execution error: {result.stderr.strip()}")
            return False, result.stdout.strip(), result.stderr.strip()
    except Exception as exc:
        logger.critical(f"Low-level catastrophic runtime failure: {str(exc)}")
        return False, "", str(exc)