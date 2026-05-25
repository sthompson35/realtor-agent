# Database-Excel Synchronization

This module provides comprehensive synchronization capabilities between SQLAlchemy database tables and Excel files for the Realtor Agent system.

## Features

- **Bidirectional Sync**: Synchronize data in both directions (Database ↔ Excel)
- **Conflict Resolution**: Multiple strategies for handling data conflicts
- **Dry Run Mode**: Test synchronization without making changes
- **Batch Processing**: Efficient handling of large datasets
- **Web Interface**: User-friendly dashboard for manual sync operations
- **CLI Tool**: Command-line interface for automated sync operations
- **Export Functionality**: Export database data to Excel files

## Architecture

```
┌─────────────────┐    ┌──────────────────┐
│   Database      │    │     Excel        │
│   (SQLAlchemy)  │◄──►│     Files        │
│                 │    │                  │
│ • Leads         │    │ • CRM Sheet      │
│ • Properties    │    │ • Deal Sheets    │
│ • Appointments  │    │ • Report Sheets  │
│ • Deals         │    │                  │
└─────────────────┘    └──────────────────┘
         ▲                       ▲
         │                       │
    ┌────┴───────────────────────┴────┐
    │                                 │
    │   Sync Engine                   │
    │   (DatabaseExcelSync)          │
    │                                 │
    └────┬───────────────────────┬────┘
         │                       │
    ┌────┴────┐             ┌────┴────┐
    │         │             │         │
    │ Web API │             │ CLI Tool│
    │         │             │         │
    └─────────┘             └─────────┘
```

## Quick Start

### Web Interface

1. Start the Realtor Agent server:
   ```bash
   cd realtor_agent
   python web_server.py
   ```

2. Open your browser to `http://localhost:5001/sync`

3. Use the web interface to:
   - View current sync status
   - Configure sync parameters
   - Run synchronization
   - Export data to Excel

### Command Line

```bash
cd realtor_agent

# Check sync status
python sync_cli.py status

# Sync leads with dry run
python sync_cli.py sync-leads --direction bidirectional --dry-run

# Sync leads from Excel to Database
python sync_cli.py sync-leads --direction excel_to_db --conflict-resolution excel_wins

# Export leads to Excel
python sync_cli.py export-leads --output my_leads.xlsx
```

## Synchronization Directions

### Bidirectional (`bidirectional`)
- Syncs data in both directions
- Adds new records from Excel to Database
- Adds new records from Database to Excel
- Resolves conflicts based on configured strategy

### Excel to Database (`excel_to_db`)
- Only imports data from Excel to Database
- Adds new Excel records to Database
- Updates existing Database records with Excel data
- Never modifies Excel file

### Database to Excel (`db_to_excel`)
- Only exports data from Database to Excel
- Adds new Database records to Excel
- Updates existing Excel records with Database data
- Never modifies Database

## Conflict Resolution Strategies

### Newest Wins (`newest_wins`)
- Compares last modified timestamps
- Keeps the most recently updated version
- Default strategy for most use cases

### Excel Wins (`excel_wins`)
- Always uses Excel data when conflicts occur
- Useful when Excel is the authoritative source
- Database data is overwritten

### Database Wins (`db_wins`)
- Always uses Database data when conflicts occur
- Useful when Database is the authoritative source
- Excel data is overwritten

### Manual Review (`manual`)
- Pauses sync when conflicts are detected
- Requires manual intervention to resolve
- Best for critical data that needs review

## API Endpoints

### GET `/api/sync/status`
Get current synchronization status.

**Response:**
```json
{
  "database": {
    "leads": 150,
    "properties": 45,
    "deals": 23
  },
  "excel": {
    "leads_crm": 142
  },
  "status": "ready"
}
```

### POST `/api/sync/leads`
Synchronize leads between database and Excel.

**Request:**
```json
{
  "direction": "bidirectional",
  "conflict_resolution": "newest_wins",
  "dry_run": false
}
```

**Response:**
```json
{
  "direction": "bidirectional",
  "records_processed": 142,
  "records_added": 8,
  "records_updated": 3,
  "records_skipped": 131,
  "conflicts": [],
  "errors": [],
  "timestamp": "2026-01-06T20:45:30.123456",
  "dry_run": false
}
```

### POST `/api/sync/export/leads`
Export leads from database to Excel file.

**Request:**
```json
{
  "filename": "leads_export_20260106.xlsx"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Exported leads to leads_export_20260106.xlsx",
  "file_path": "leads_export_20260106.xlsx"
}
```

## Configuration

The sync behavior can be configured via `sync_config.ini`:

```ini
[sync]
default_direction = "bidirectional"
default_conflict_resolution = "newest_wins"
batch_size = 100

[leads_mapping]
lead_id = "Lead ID"
name = "Owner Name"
email = "Email"
# ... more mappings
```

## Data Mapping

### Leads Table Mapping
| Database Field | Excel Column | Description |
|----------------|--------------|-------------|
| lead_id | Lead ID | Unique identifier |
| name | Owner Name | Contact name |
| email | Email | Email address |
| phone | Phone | Phone number |
| source | Source (List) | Lead source |
| status | Status | Lead status |
| last_contact | Last Contact | Last contact date |
| mailing_address | Mailing Address | Mailing address |
| property_address | Property Address/APN | Property address |
| market | Market | Market/location |

## Best Practices

### 1. Always Test with Dry Run
```bash
python sync_cli.py sync-leads --dry-run
```

### 2. Backup Before Major Syncs
```bash
cp Land_and_Build_Flipping_System_v2.xlsx backup.xlsx
```

### 3. Use Appropriate Conflict Resolution
- Use `newest_wins` for regular syncs
- Use `excel_wins` when Excel is your primary data entry
- Use `manual` for critical business data

### 4. Monitor Sync Results
Check the results for:
- Number of records processed/added/updated
- Any conflicts that occurred
- Errors that need attention

### 5. Schedule Regular Syncs
Set up automated syncs for regular data consistency:
```bash
# Daily sync at 2 AM
crontab -e
0 2 * * * cd /path/to/realtor_agent && python sync_cli.py sync-leads
```

## Troubleshooting

### Common Issues

**1. Excel File Locked**
```
Error: Excel file is currently open in another application
```
**Solution:** Close Excel and try again

**2. Database Connection Failed**
```
Error: Unable to connect to database
```
**Solution:** Check database configuration and connectivity

**3. Permission Denied**
```
Error: Permission denied when writing to Excel file
```
**Solution:** Check file permissions and close any applications using the file

**4. Data Type Mismatch**
```
Error: Cannot convert value to expected type
```
**Solution:** Check data formats in Excel match expected database types

### Debug Mode

Enable debug logging for detailed sync information:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Recovery

If a sync operation fails partway through:

1. Check the error message for specific issues
2. Run with `--dry-run` to verify the operation
3. Manually resolve any data conflicts
4. Retry the sync operation

## Security Considerations

- **Data Validation**: All data is validated before sync operations
- **Transaction Safety**: Database operations use transactions for consistency
- **Access Control**: Web interface requires authentication (when implemented)
- **Audit Trail**: All sync operations are logged with timestamps

## Future Enhancements

- **Scheduled Syncs**: Automated periodic synchronization
- **Real-time Sync**: Live synchronization for collaborative editing
- **Advanced Conflict Resolution**: AI-powered conflict resolution
- **Multi-table Sync**: Synchronize properties, deals, and appointments
- **Sync History**: Track all sync operations and changes
- **Rollback Capability**: Undo sync operations if needed

## Support

For issues or questions about the sync functionality:

1. Check the logs in `logs/sync.log`
2. Run diagnostic commands:
   ```bash
   python sync_cli.py status --verbose
   ```
3. Review the configuration in `sync_config.ini`
4. Check the web interface at `/sync` for visual diagnostics

---

© Shylow Thompson. LLC 2026 - All Rights Reserved