# Storage Structure

## Overview

All application-generated files are stored in the `storage/` folder located at:
```
C:\Users\333305\Downloads\MCP_Application\nttdata_regulatory_reporting_system\storage
```

This centralized storage approach ensures:
- Easy backup and restore
- Simple cleanup
- Clear separation of code and data
- Consistent file organization

## Directory Structure

```
storage/
├── chroma_data/              # ChromaDB vector database
│   ├── collections/          # Vector collections
│   └── indexes/              # Vector indexes
│
├── documents/                # Uploaded regulatory documents
│   ├── fca/                  # FCA documents
│   ├── pra/                  # PRA documents
│   ├── boe/                  # Bank of England documents
│   └── other/                # Other regulatory bodies
│
├── reports/                  # Generated reports
│   ├── submissions/          # Submitted reports
│   ├── validation/           # Validation reports
│   ├── drafts/               # Draft reports
│   └── approved/             # Approved reports
│
├── logs/                     # Application logs
│   ├── application/          # Main application logs
│   │   ├── app.log           # Current application log
│   │   ├── error.log         # Error log
│   │   └── daily.log         # Daily rotating log
│   ├── audit/                # Audit logs (7-year retention)
│   │   └── audit.log         # Audit trail
│   └── agents/               # Agent-specific logs
│       ├── compliance.log
│       ├── interpreter.log
│       └── ...               # One log per agent
│
├── audit_logs/               # Structured audit data
│
├── generated_code/           # AI-generated code
│   ├── sql/                  # Generated SQL scripts
│   ├── python/               # Generated Python code
│   └── tests/                # Generated test files
│
├── graphrag/                 # GraphRAG data
│   ├── graphs/               # Knowledge graphs
│   ├── communities/          # Graph communities
│   ├── entities/             # Extracted entities
│   └── analysis/             # Analysis results
│
├── embeddings/               # Embedding data
│   ├── vectors/              # Vector embeddings
│   ├── tiktoken_cache/       # Token cache
│   └── indexes/              # Embedding indexes
│
├── workflows/                # Workflow data
│   ├── definitions/          # Workflow definitions
│   ├── executions/           # Execution state
│   ├── state/                # Current state
│   └── history/              # Execution history
│
├── files/                    # File uploads
│   ├── uploads/              # Raw uploads
│   ├── processed/            # Processed files
│   └── archived/             # Archived files
│
├── cache/                    # Application cache
│   ├── api/                  # API response cache
│   ├── embeddings/           # Embedding cache
│   └── queries/              # Query cache
│
├── backups/                  # Backups
│   ├── daily/                # Daily backups
│   ├── weekly/               # Weekly backups
│   └── monthly/              # Monthly backups
│
└── temp/                     # Temporary files
    ├── uploads/              # Temp upload files
    ├── processing/           # Files being processed
    └── exports/              # Temp export files
```

## Configuration

Storage paths are configured in `backend/app/core/config.py`:

```python
# Base storage path
STORAGE_PATH: Path = Path("./storage")

# ChromaDB path (inside storage)
CHROMA_PATH: Path = Path("./storage/chroma_data")
```

Override in `.env` file:
```bash
STORAGE_PATH=./storage
CHROMA_PATH=./storage/chroma_data
```

## Initialization

Storage directories are automatically created on application startup via:
```python
from scripts.setup_storage import setup_storage
setup_storage()
```

## File Management

### Document Storage
All uploaded regulatory documents are stored in:
```
storage/documents/{regulator}/{filename}
```

### Report Generation
Generated reports are stored in:
```
storage/reports/submissions/{report_name}_{date}.pdf
```

### Log Files
- **Application logs**: `storage/logs/application/app.log`
- **Error logs**: `storage/logs/application/error.log`
- **Audit logs**: `storage/logs/audit/audit.log` (7-year retention)
- **Agent logs**: `storage/logs/agents/{agent_name}.log`

### ChromaDB Data
Vector database files are stored in:
```
storage/chroma_data/collections/{collection_name}/
```

### Generated Code
AI-generated code is versioned and stored in:
```
storage/generated_code/{sql|python}/{code_id}_{version}.{sql|py}
```

## Backup Strategy

### Automatic Backups
The cleanup task (runs every 24 hours) can be extended to create backups:

1. **Daily**: Keep last 7 days
2. **Weekly**: Keep last 4 weeks
3. **Monthly**: Keep last 12 months

### Manual Backup
To backup the entire storage folder:
```bash
# Windows
xcopy /E /I storage storage_backup_2024-04-02

# Linux/Mac
cp -r storage storage_backup_2024-04-02
```

## Cleanup

### Automatic Cleanup
The background cleanup task removes:
- Expired sessions (> 7 days)
- Old cache entries (> 1 hour)
- Rate limit records (> 1 hour)
- Temp files (> 1 day)

### Manual Cleanup
To clean temporary files:
```bash
# Windows
rmdir /S /Q storage\temp
mkdir storage\temp\uploads storage\temp\processing storage\temp\exports

# Linux/Mac
rm -rf storage/temp/*
mkdir -p storage/temp/{uploads,processing,exports}
```

## Security

### File Permissions
- Ensure proper file permissions on the storage folder
- Limit access to authorized users only
- Use encryption for sensitive documents

### Audit Logs
- Audit logs are append-only
- 7-year retention for compliance
- Never delete audit logs

### Sensitive Data
Files containing sensitive data should be:
- Encrypted at rest
- Access logged in audit trail
- Backed up securely

## Disk Space Management

### Monitoring
Monitor disk space usage:
```python
from pathlib import Path
import shutil

storage_path = Path("./storage")
total, used, free = shutil.disk_usage(storage_path)

print(f"Total: {total // (2**30)} GB")
print(f"Used: {used // (2**30)} GB")
print(f"Free: {free // (2**30)} GB")
```

### Recommendations
- **Minimum**: 10 GB free space
- **Recommended**: 50 GB for production
- **Archive**: Move old files to cold storage after 1 year

## Troubleshooting

### Storage Initialization Fails
```bash
# Manually create storage directories
cd backend
python scripts/setup_storage.py
```

### Permission Denied
```bash
# Windows: Run as Administrator
# Linux/Mac:
chmod -R 755 storage/
```

### Disk Full
1. Check disk space: `df -h` (Linux/Mac) or `dir` (Windows)
2. Clean temp files: Remove `storage/temp/*`
3. Archive old files: Move old documents to external storage
4. Compress logs: Archive logs older than 30 days

## Migration

### Moving Storage Location
To move the storage folder:

1. Stop the application
2. Update `.env`:
   ```bash
   STORAGE_PATH=/new/path/to/storage
   CHROMA_PATH=/new/path/to/storage/chroma_data
   ```
3. Copy existing storage:
   ```bash
   cp -r storage /new/path/to/storage
   ```
4. Restart the application

## Related Files

- Configuration: `backend/app/core/config.py`
- Setup script: `backend/scripts/setup_storage.py`
- Logging config: `backend/app/core/logging.py`
- .gitignore: `.gitignore`
- Environment: `backend/.env.example`

---

**Last Updated**: 2026-04-02  
**Version**: 1.0.0
