"""Command-line router for the Linux User & Group Management System."""

import argparse
import sys
import getpass
from utils.permissions import enforce_root
from utils.history import AuditHistory
from managers.user_manager import UserManager
from managers.group_manager import GroupManager
from managers.password_manager import PasswordManager
from managers.backup_manager import BackupManager
from managers.export_manager import ExportManager

def main() -> None:
    """Orchestrates system arguments parsing pipelines and delegates functional pathways."""
    parser = argparse.ArgumentParser(
        description="Production Linux Identity Infrastructure Management Suite Module Platform Engine Control Layer."
    )
    parser.add_argument("--dry-run", action="store_true", help="Execute processing flow checks without committing alterations.")
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Administrative structural functional contexts.")

    # User Management Commands
    subparsers.add_parser("list-users", help="List out filtered operational identities.")
    
    create_user_parser = subparsers.add_parser("create-user", help="Provision system account context layers.")
    create_user_parser.add_argument("username", help="System valid targeting identifier sequence.")
    create_user_parser.add_argument("--home", help="Alternative execution storage pathway assignment location maps.")
    create_user_parser.add_argument("--shell", help="Direct absolute executable command interpretation binary destination mapping path.")

    delete_user_parser = subparsers.add_parser("delete-user", help="Purge identities from internal system records structural layers.")
    delete_user_parser.add_argument("username", help="Account identifier context target.")
    delete_user_parser.add_argument("--keep-home", action="store_true", help="Preserve associated system storage partitions.")

    user_info_parser = subparsers.add_parser("info", help="Expose localized properties mapped down to system users.")
    user_info_parser.add_argument("username", help="Query search string.")

    # Password Management Commands
    passwd_parser = subparsers.add_parser("change-password", help="Update target credential parameters cleanly.")
    passwd_parser.add_argument("username", help="Target user context configuration space name mapping entity.")

    lock_parser = subparsers.add_parser("lock-user", help="Apply system structural lockouts against target identity mappings.")
    lock_parser.add_argument("username", help="Target username.")

    unlock_parser = subparsers.add_parser("unlock-user", help="Restore standard session capabilities to locked accounts.")
    unlock_parser.add_argument("username", help="Target username.")

    force_reset_parser = subparsers.add_parser("force-reset", help="Force credential resets on subsequent shell allocations.")
    force_reset_parser.add_argument("username", help="Target username.")

    # Group Management Commands
    subparsers.add_parser("list-groups", help="Read system group configurations out of active environments.")
    
    create_group_parser = subparsers.add_parser("create-group", help="Instantiate unique structural protection group contexts.")
    create_group_parser.add_argument("group_name", help="Validation-compliant system group name target designation.")

    delete_group_parser = subparsers.add_parser("delete-group", help="Purge isolated structural classification target tags.")
    delete_group_parser.add_argument("group_name", help="Target group name.")

    add_member_parser = subparsers.add_parser("add-group", help="Add an active user account into a targeted group.")
    add_member_parser.add_argument("username", help="Target username.")
    add_member_parser.add_argument("group_name", help="Target group name.")

    remove_member_parser = subparsers.add_parser("remove-group", help="Remove user memberships from isolated group configurations.")
    remove_member_parser.add_argument("username", help="Target username.")
    remove_member_parser.add_argument("group_name", help="Target group name.")

    # Infrastructure Task Operations
    subparsers.add_parser("backup", help="Capture system core credential databases snapshot backups.")
    subparsers.add_parser("export", help="Compile and export tabular telemetry matrices reporting files out of local runtime scopes.")
    subparsers.add_parser("history", help="Expose audited structural metrics from prior run events loops execution pipelines.")

    parsed_args = parser.parse_args()
    invoking_user = getpass.getuser()

    # Enforce root structural controls across mutating system changes
    if parsed_args.command not in ["list-users", "list-groups", "info", "history"]:
        enforce_root()

    status_flag = "FAILED"

    try:
        if parsed_args.command == "list-users":
            users = UserManager.list_all_users()
            print(f"{'USERNAME':<15} {'UID':<6} {'GID':<6} {'SHELL':<20} {'HOME'}")
            print("-" * 70)
            for user in users:
                print(f"{user['username']:<15} {user['uid']:<6} {user['gid']:<6} {user['shell']:<20} {user['home']}")
            status_flag = "SUCCESS"

        elif parsed_args.command == "create-user":
            success = UserManager.create_user(parsed_args.username, parsed_args.home, parsed_args.shell, parsed_args.dry_run)
            status_flag = "SUCCESS" if success else "FAILED"
            print(f"User creation outcome: {status_flag}")

        elif parsed_args.command == "delete-user":
            success = UserManager.delete_user(parsed_args.username, not parsed_args.keep_home, parsed_args.dry_run)
            status_flag = "SUCCESS" if success else "FAILED"
            print(f"User deletion outcome: {status_flag}")

        elif parsed_args.command == "info":
            data = UserManager.search_user(parsed_args.username)
            if data:
                print("\n[USER CONFIGURATION PROPERTIES METRICS]")
                for k, v in data.items():
                    print(f" -> {k.upper():<12}: {v}")
                status_flag = "SUCCESS"
            else:
                print("[ERROR] Requested target search target record yielded empty arrays.")

        elif parsed_args.command == "change-password":
            pwd_input = getpass.getpass("Enter secure targeted clearance password parameters: ")
            pwd_confirm = getpass.getpass("Confirm structural clearance identity parameters: ")
            if pwd_input != pwd_confirm:
                print("[CRITICAL] Input mismatches verified. Execution dropped.")
                sys.exit(1)
            success = PasswordManager.change_password(parsed_args.username, pwd_input, parsed_args.dry_run)
            status_flag = "SUCCESS" if success else "FAILED"

        elif parsed_args.command == "lock-user":
            success = PasswordManager.lock_account(parsed_args.username, parsed_args.dry_run)
            status_flag = "SUCCESS" if success else "FAILED"

        elif parsed_args.command == "unlock-user":
            success = PasswordManager.unlock_account(parsed_args.username, parsed_args.dry_run)
            status_flag = "SUCCESS" if success else "FAILED"

        elif parsed_args.command == "force-reset":
            success = PasswordManager.force_password_reset(parsed_args.username, parsed_args.dry_run)
            status_flag = "SUCCESS" if success else "FAILED"

        elif parsed_args.command == "list-groups":
            groups = GroupManager.list_groups()
            print(f"{'GROUP NAME':<20} {'GID':<8} {'MEMBERS'}")
            print("-" * 60)
            for g in groups:
                print(f"{g['group_name']:<20} {g['gid']:<8} {g['members']}")
            status_flag = "SUCCESS"

        elif parsed_args.command == "create-group":
            success = GroupManager.create_group(parsed_args.group_name, parsed_args.dry_run)
            status_flag = "SUCCESS" if success else "FAILED"

        elif parsed_args.command == "delete-group":
            success = GroupManager.delete_group(parsed_args.group_name, parsed_args.dry_run)
            status_flag = "SUCCESS" if success else "FAILED"

        elif parsed_args.command == "add-group":
            success = GroupManager.add_user_to_group(parsed_args.username, parsed_args.group_name, parsed_args.dry_run)
            status_flag = "SUCCESS" if success else "FAILED"

        elif parsed_args.command == "remove-group":
            success = GroupManager.remove_user_from_group(parsed_args.username, parsed_args.group_name, parsed_args.dry_run)
            status_flag = "SUCCESS" if success else "FAILED"

        elif parsed_args.command == "backup":
            success = BackupManager.execute_backup(parsed_args.dry_run)
            status_flag = "SUCCESS" if success else "FAILED"

        elif parsed_args.command == "export":
            success = ExportManager.export_data()
            status_flag = "SUCCESS" if success else "FAILED"

        elif parsed_args.command == "history":
            history_logs = AuditHistory.read_history()
            print(f"{'TIMESTAMP':<20} {'COMMAND':<15} {'USER':<12} {'STATUS'}")
            print("-" * 60)
            for logs in history_logs[-20:]:  # Limit display to last 20 actions
                print(f"{logs['timestamp'][:19]:<20} {logs['command']:<15} {logs['user']:<12} {logs['status']}")
            status_flag = "SUCCESS"

    except Exception as exc:
        print(f"[CRITICAL APPLICATION FAILURE]: {str(exc)}")
        status_flag = f"CRASH: {type(exc).__name__}"
    finally:
        # Record metrics telemetry into security transactional logs
        AuditHistory.log_action(
            command=parsed_args.command,
            arguments=sys.argv[1:],
            executed_by=invoking_user,
            status=status_flag
        )

if __name__ == "__main__":
    main()