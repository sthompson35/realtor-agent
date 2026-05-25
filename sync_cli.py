#!/usr/bin/env python3
"""
Database to Excel Synchronization CLI Tool
Command-line interface for synchronizing data between database and Excel files.

Usage:
    python sync_cli.py --help
    python sync_cli.py status
    python sync_cli.py sync-leads --direction bidirectional --dry-run
    python sync_cli.py export-leads --output my_leads.xlsx

© Shylow Thompson. LLC 2026 - All Rights Reserved
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the realtor_agent path to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from realtor_agent.utils.sync import DatabaseExcelSync, SyncDirection, ConflictResolution


def print_status(status):
    """Print synchronization status in a formatted way."""
    print("🔄 Database-Excel Synchronization Status")
    print("=" * 50)

    if status.get('error'):
        print(f"❌ Error: {status['error']}")
        return

    print("📊 Database Records:")
    print(f"   • Leads: {status['database']['leads']}")
    print(f"   • Properties: {status['database']['properties']}")
    print(f"   • Deals: {status['database']['deals']}")

    print("\n📋 Excel Records:")
    print(f"   • CRM Leads: {status['excel']['leads_crm']}")

    print(f"\n📈 Status: {status.get('status', 'unknown')}")


def print_sync_result(result):
    """Print synchronization result in a formatted way."""
    print("🔄 Synchronization Results")
    print("=" * 50)
    print(f"⏰ Completed at: {result['timestamp']}")
    print(f"📍 Direction: {result['direction']}")
    print(f"🧪 Dry Run: {result['dry_run']}")

    print("\n📊 Summary:")
    print(f"   • Records Processed: {result['records_processed']}")
    print(f"   • Records Added: {result['records_added']}")
    print(f"   • Records Updated: {result['records_updated']}")
    print(f"   • Records Skipped: {result['records_skipped']}")

    if result['conflicts']:
        print(f"\n⚠️  Conflicts: {len(result['conflicts'])}")
        for conflict in result['conflicts'][:5]:  # Show first 5 conflicts
            print(f"   • Lead ID {conflict['key']}: {conflict['resolution']}")
        if len(result['conflicts']) > 5:
            print(f"   ... and {len(result['conflicts']) - 5} more")

    if result['errors']:
        print(f"\n❌ Errors: {len(result['errors'])}")
        for error in result['errors'][:3]:  # Show first 3 errors
            print(f"   • {error}")
        if len(result['errors']) > 3:
            print(f"   ... and {len(result['errors']) - 3} more")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Database to Excel Synchronization Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sync_cli.py status
  python sync_cli.py sync-leads --direction bidirectional --dry-run
  python sync_cli.py sync-leads --direction excel_to_db --conflict-resolution excel_wins
  python sync_cli.py export-leads --output my_export.xlsx
  python sync_cli.py export-leads  # Uses auto-generated filename
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Status command
    status_parser = subparsers.add_parser('status', help='Show synchronization status')
    status_parser.add_argument(
        '--json',
        action='store_true',
        help='Output result as JSON'
    )

    # Sync leads command
    sync_parser = subparsers.add_parser('sync-leads', help='Synchronize leads between database and Excel')
    sync_parser.add_argument(
        '--direction',
        choices=['bidirectional', 'excel_to_db', 'db_to_excel'],
        default='bidirectional',
        help='Synchronization direction (default: bidirectional)'
    )
    sync_parser.add_argument(
        '--conflict-resolution',
        choices=['newest_wins', 'excel_wins', 'db_wins', 'manual'],
        default='newest_wins',
        help='How to resolve conflicts (default: newest_wins)'
    )
    sync_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform dry run without making changes'
    )
    sync_parser.add_argument(
        '--json',
        action='store_true',
        help='Output result as JSON'
    )

    # Export leads command
    export_parser = subparsers.add_parser('export-leads', help='Export leads from database to Excel file')
    export_parser.add_argument(
        '--output', '-o',
        help='Output filename (default: auto-generated)'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        sync = DatabaseExcelSync()

        if args.command == 'status':
            status = sync.get_sync_status()
            if args.json:
                print(json.dumps(status, indent=2))
            else:
                print_status(status)

        elif args.command == 'sync-leads':
            # Convert string arguments to enums
            direction_map = {
                'bidirectional': SyncDirection.BIDIRECTIONAL,
                'excel_to_db': SyncDirection.EXCEL_TO_DB,
                'db_to_excel': SyncDirection.DB_TO_EXCEL
            }

            resolution_map = {
                'newest_wins': ConflictResolution.NEWEST_WINS,
                'excel_wins': ConflictResolution.EXCEL_WINS,
                'db_wins': ConflictResolution.DB_WINS,
                'manual': ConflictResolution.MANUAL
            }

            result = sync.sync_leads_crm(
                direction=direction_map[args.direction],
                conflict_resolution=resolution_map[args.conflict_resolution],
                dry_run=args.dry_run
            )

            # Convert to dict for JSON output
            result_dict = {
                'direction': result.direction.value,
                'records_processed': result.records_processed,
                'records_added': result.records_added,
                'records_updated': result.records_updated,
                'records_skipped': result.records_skipped,
                'conflicts': result.conflicts,
                'errors': result.errors,
                'timestamp': result.timestamp.isoformat(),
                'dry_run': args.dry_run
            }

            if getattr(args, 'json', False):
                print(json.dumps(result_dict, indent=2))
            else:
                print_sync_result(result_dict)

        elif args.command == 'export-leads':
            output_path = args.output if args.output else None
            exported_file = sync.export_leads_to_excel(Path(output_path) if output_path else None)
            print(f"✅ Leads exported to: {exported_file}")

    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()