# Storage Migration - Centralized Storage Structure

## Summary of Changes

All application-generated files have been configured to store in a centralized `storage/` folder located at:
```
C:\Users\333305\Downloads\MCP_Application\nttdata_regulatory_reporting_system\storage
```

## What Changed

### 1. Configuration (config.py)
**Before:**
```python
STORAGE_PATH: Path = Path("./storage")
CHROMA_PATH: Path = Path("./chroma_data")  # Outside storage folder
```

**After:**
```python
STORAGE_PATH: Path = Path("./storage")
CHROMA_PATH: Path = Path("./storage/chroma_data")  # Inside storage folder
```

### 2. Logging (logging.py)
**Before:**
```python
log_dir = Path(settings.BASE_DIR) / "logs"  # In project root
```

**After:**
```python
log_dir = Path(settings.STORAGE_PATH) / "logs" / "application"  # In storage folder
```

All log types now store in storage:
- Application logs: `storage/logs/application/`
- Agent logs: `storage/logs/agents/`
- Audit logs: `storage/logs/audit/`

### 3. Storage Setup (setup_storage.py)
Added new directories:
- `chroma_data/collections` - ChromaDB collections
- `chroma_data/indexes` - ChromaDB indexes
- `logs/application` - Application logs
- `logs/audit` - Audit logs
- `logs/agents` - Agent logs
- `logs/daily` - Daily rotating logs
- `generated_code/tests` - Generated test files
- `reports/drafts` - Draft reports
- `reports/approved` - Approved reports
- `files/uploads` - File uploads
- `files/processed` - Processed files
- `files/archived` - Archived files
- `cache/api` - API cache
- `cache/embeddings` - Embedding cache
- `cache/queries` - Query cache
- `temp/exports` - Temporary export files

### 4. Environment (.env.example)
Updated documentation:
```bash
# Storage - All application files stored in this folder
STORAGE_PATH=./storage

# ChromaDB - Vector database stored inside storage folder
CHROMA_PATH=./storage/chroma_data
```

### 5. Git Ignore (.gitignore)
Updated to properly ignore storage folder:
```
# Storage folder - all application-generated files
storage/
!storage/.gitkeep
```

## Directory Structure

```
storage/
├── chroma_data/              ✅ ChromaDB vector database
├── documents/                ✅ Regulatory documents
├── reports/                  ✅ Generated reports
├── logs/                     ✅ All logs (application, audit, agents)
├── audit_logs/               ✅ Structured audit data
├── generated_code/           ✅ AI-generated code
├── graphrag/                 ✅ Knowledge graphs
├── embeddings/               ✅ Vector embeddings
├── workflows/                ✅ Workflow data
├── files/                    ✅ File uploads and processing
├── cache/                    ✅ Application cache
├── backups/                  ✅ Backups
└── temp/                     ✅ Temporary files
```

## Benefits

### 1. **Centralized Management**
- All application data in one location
- Easy to backup entire storage folder
- Simple to restore from backup

### 2. **Clean Project Structure**
- No scattered data files in project root
- Clear separation of code and data
- Better organization

### 3. **Easy Deployment**
- Mount single storage volume in Docker/K8s
- Simple to configure different storage backends
- Easy to share storage across instances

### 4. **Simple Cleanup**
```bash
# Clean all application data
rm -rf storage/*

# Or selectively clean
rm -rf storage/temp/*
rm -rf storage/cache/*
```

### 5. **Better Security**
- Set permissions on single folder
- Encrypt entire storage folder
- Audit all file access in one place

## Migration Steps

### For Fresh Installation
No migration needed! Just run:
```bash
cd backend
python app.py
```

Storage structure will be created automatically.

### For Existing Installation

If you have data in old locations (e.g., `chroma_data/` in root):

1. **Stop the application**
   ```bash
   # Stop any running instance
   ```

2. **Backup existing data**
   ```bash
   # Windows
   xcopy /E /I chroma_data chroma_data_backup
   
   # Linux/Mac
   cp -r chroma_data chroma_data_backup
   ```

3. **Move data to new location**
   ```bash
   # Windows
   mkdir storage\chroma_data
   xcopy /E /I chroma_data storage\chroma_data
   
   # Linux/Mac
   mkdir -p storage/chroma_data
   mv chroma_data/* storage/chroma_data/
   ```

4. **Update .env file** (if using custom paths)
   ```bash
   CHROMA_PATH=./storage/chroma_data
   ```

5. **Start the application**
   ```bash
   cd backend
   python app.py
   ```

6. **Verify data migration**
   - Check logs: `storage/logs/application/app.log`
   - Check ChromaDB: `storage/chroma_data/`
   - Test API endpoints

7. **Remove old data** (after verification)
   ```bash
   # Windows
   rmdir /S /Q chroma_data_backup
   
   # Linux/Mac
   rm -rf chroma_data_backup
   ```

## Verification

### 1. Check Storage Structure
```bash
# Windows
dir storage /S

# Linux/Mac
tree storage
```

### 2. Check Logs
```bash
# Application is writing logs
cat storage/logs/application/app.log

# Audit logs working
cat storage/logs/audit/audit.log
```

### 3. Check ChromaDB
```python
from app.db.chroma_db import get_chroma_client
client = get_chroma_client()
print(client.list_collections())
```

### 4. Check File Permissions
```bash
# Linux/Mac
ls -la storage/

# Should show proper permissions
```

## Rollback

If you need to rollback:

1. Stop the application
2. Restore from backup
3. Update config.py:
   ```python
   CHROMA_PATH: Path = Path("./chroma_data")  # Old location
   ```
4. Update logging.py:
   ```python
   log_dir = Path(settings.BASE_DIR) / "logs"  # Old location
   ```
5. Restart application

## Backup Strategy

### Daily Backup
```bash
# Backup entire storage folder
tar -czf backup_$(date +%Y%m%d).tar.gz storage/
```

### Selective Backup
```bash
# Backup only critical data
tar -czf backup_critical_$(date +%Y%m%d).tar.gz \
  storage/documents/ \
  storage/reports/ \
  storage/logs/audit/
```

### Cloud Backup
```bash
# AWS S3
aws s3 sync storage/ s3://your-bucket/storage/

# Azure Blob Storage
az storage blob upload-batch -d storage -s ./storage/

# Google Cloud Storage
gsutil -m rsync -r storage/ gs://your-bucket/storage/
```

## Monitoring

### Disk Space
```python
import shutil
total, used, free = shutil.disk_usage("storage")
print(f"Storage: {used / (2**30):.2f} GB / {total / (2**30):.2f} GB")
```

### File Count
```bash
# Windows
dir storage /S | find /C "File(s)"

# Linux/Mac
find storage -type f | wc -l
```

### Largest Directories
```bash
# Windows
dir storage /S | sort /R

# Linux/Mac
du -sh storage/* | sort -rh | head -10
```

## Support

For issues or questions:
1. Check `STORAGE_STRUCTURE.md` for detailed documentation
2. Check logs in `storage/logs/application/app.log`
3. Review `VALIDATION_REPORT.md` for system status

---

**Migration Date**: 2026-04-02  
**Status**: ✅ Complete  
**Version**: 1.0.0
