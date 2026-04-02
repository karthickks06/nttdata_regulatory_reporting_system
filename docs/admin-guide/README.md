# Administrator Guide

## System Administration

This guide covers administrative tasks for the NTT Data Regulatory Reporting System.

## Initial Setup

### Database Configuration

1. Create PostgreSQL database:
```bash
createdb regulatory_reporting
```

2. Configure `.env`:
```bash
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=reg_user
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=regulatory_reporting
```

3. Run initialization:
```bash
cd backend
python app.py
```

This automatically:
- Creates all database tables
- Seeds initial data
- Creates storage directories
- Initializes ChromaDB

### Storage Configuration

Storage directories are created automatically in `./storage/`:

- `documents/` - Regulatory documents
- `reports/` - Generated reports
- `audit_logs/` - Audit trails
- `generated_code/` - AI-generated code
- `graphrag/` - Knowledge graphs
- `embeddings/` - Vector embeddings
- `workflows/` - Workflow data
- `backups/` - Automated backups
- `temp/` - Temporary files

### ChromaDB Setup

ChromaDB is initialized automatically with two collections:

1. `regulatory_documents` - Document embeddings
2. `knowledge_graph` - Entity relationships

Data persists in `./chroma_db/` directory.

## User Management

### Creating Users

Via API:
```bash
POST /api/v1/users
{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "User Name",
  "role_ids": ["<role_id>"]
}
```

Via Admin UI:
1. Navigate to "Admin" > "Users"
2. Click "Create User"
3. Fill in details
4. Assign roles
5. Click "Save"

### Managing Roles

Default roles:
- Admin
- Business Analyst
- Developer
- Analyst
- Approver
- Viewer

To create custom roles:
1. Navigate to "Admin" > "Roles"
2. Click "Create Role"
3. Set name and description
4. Assign permissions
5. Click "Save"

### Permission Management

Permissions are resource-action pairs:
- Format: `resource:action`
- Example: `reports:read`, `users:create`

To assign permissions to roles:
1. Navigate to "Admin" > "Roles"
2. Select role
3. Click "Manage Permissions"
4. Select/deselect permissions
5. Click "Save"

## System Monitoring

### Health Checks

Check system health:
```bash
GET /api/v1/admin/system/health
```

Response:
```json
{
  "status": "healthy",
  "components": {
    "database": "healthy",
    "chromadb": "healthy"
  }
}
```

### Metrics Dashboard

View metrics at "Admin" > "System Monitoring":

- User count
- Document count
- Active workflows
- Report count
- Agent activity
- Storage usage

### Performance Monitoring

Monitor via API:
```bash
GET /api/v1/admin/system/metrics
```

Key metrics:
- Request rate
- Response times
- Error rates
- Database connections
- Cache hit rates

## Audit Logging

### Viewing Audit Logs

Via UI:
1. Navigate to "Admin" > "Audit Logs"
2. Apply filters:
   - Date range
   - User
   - Action type
   - Resource
   - Status
3. Export results

Via API:
```bash
GET /api/v1/admin/audit/logs?days=7&action=CREATE
```

### Audit Log Storage

Logs are stored in two places:

1. **Database**: Recent logs (queryable)
2. **Files**: Daily JSONL files in `storage/audit_logs/YYYY/MM/`

### Audit Log Cleanup

Clean up old database logs (files are retained):

```bash
POST /api/v1/admin/audit/cleanup
{
  "days_to_keep": 90
}
```

Recommended: Keep 90 days in database, archive files indefinitely.

## Workflow Management

### Active Workflows

Monitor active workflows:
```bash
GET /api/v1/admin/workflows/active
```

View details:
- Execution ID
- Current step
- Progress
- Start time
- Assigned agents

### Workflow History

Query workflow history:
```bash
GET /api/v1/admin/workflows/history?year=2026&month=4
```

### Workflow Cleanup

Clean up old workflow files:
```bash
POST /api/v1/admin/workflows/cleanup
{
  "days_to_keep": 90
}
```

## Cache Management

### Cache Statistics

View cache stats:
```bash
GET /api/v1/admin/cache/stats
```

Shows:
- Total entries
- Active entries
- Expired entries
- Memory usage

### Cache Clearing

Clear expired entries only:
```bash
POST /api/v1/admin/cache/clear
{
  "expired_only": true
}
```

Clear all cache:
```bash
POST /api/v1/admin/cache/clear
{
  "expired_only": false
}
```

## Background Tasks

### Task Queue Status

Monitor background tasks:
```bash
GET /api/v1/admin/tasks/queue
```

View:
- Pending tasks
- Running tasks
- Completed tasks
- Failed tasks

### Task Types

- Document processing
- Agent execution
- Report generation
- Notification sending
- Cleanup jobs

## Agent Configuration

### Agent Settings

Configure agents at `backend/app/agents/config/settings.py`:

```python
AGENT_SETTINGS = {
    "compliance_agent": {
        "model": "gpt-4-turbo",
        "temperature": 0.1,
        "max_tokens": 4000
    },
    "interpreter_agent": {
        "model": "gpt-4-turbo",
        "temperature": 0.2,
        "max_tokens": 3000
    }
}
```

### Agent Prompts

Customize prompts at `backend/app/agents/config/prompts.py`.

### Agent Monitoring

View agent activity:
1. Navigate to "Admin" > "Agents"
2. Select agent
3. View:
   - Execution count
   - Success rate
   - Average duration
   - Recent errors

## Database Management

### Manual Migrations

No Alembic! Use manual SQL migrations:

1. Update model in `backend/app/models/`
2. Create migration file in `backend/migrations/XXX_name.sql`
3. Apply migration:
```bash
psql -U reg_user -d regulatory_reporting < migrations/XXX_name.sql
```

4. Update `backend/migrations/README.md`

### Database Backups

#### Automated Backups

Configure in app.py:
```python
BACKUP_SCHEDULE = {
    "daily": "02:00",  # 2 AM daily
    "weekly": "Sunday",
    "monthly": "1st"
}
```

#### Manual Backup

```bash
pg_dump -U reg_user regulatory_reporting > backup_$(date +%Y%m%d).sql
```

#### Restore Backup

```bash
psql -U reg_user regulatory_reporting < backup_20260401.sql
```

### Database Maintenance

#### Vacuum

```bash
psql -U reg_user -d regulatory_reporting -c "VACUUM ANALYZE;"
```

#### Reindex

```bash
psql -U reg_user -d regulatory_reporting -c "REINDEX DATABASE regulatory_reporting;"
```

## Security

### Password Policy

Configure in `backend/app/core/security.py`:

```python
PASSWORD_POLICY = {
    "min_length": 12,
    "require_uppercase": True,
    "require_lowercase": True,
    "require_numbers": True,
    "require_special": True,
    "expiry_days": 90
}
```

### Session Management

JWT tokens:
- Access token: 30 minutes
- Refresh token: 7 days

Configure in `.env`:
```bash
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Rate Limiting

Rate limits per endpoint:
- Authentication: 5/minute
- Document upload: 10/hour
- Report generation: 20/hour
- Other endpoints: 100/minute

Configure in `backend/app/core/config.py`.

### IP Whitelisting

Configure allowed IPs in `.env`:
```bash
ALLOWED_IPS=["192.168.1.0/24", "10.0.0.0/8"]
```

## Troubleshooting

### Application Won't Start

1. Check PostgreSQL is running:
```bash
pg_isready
```

2. Check database exists:
```bash
psql -U reg_user -l | grep regulatory_reporting
```

3. Check logs:
```bash
tail -f backend/logs/app.log
```

### ChromaDB Issues

Delete and reinitialize:
```bash
rm -rf chroma_db/
python backend/app.py  # Recreates collections
```

### Storage Issues

Check disk space:
```bash
df -h
```

Clean up temp files:
```bash
rm -rf storage/temp/*
```

### Performance Issues

1. Check database performance:
```bash
psql -U reg_user -d regulatory_reporting -c "SELECT * FROM pg_stat_activity;"
```

2. Check cache hit rates:
```bash
GET /api/v1/admin/cache/stats
```

3. Monitor agent execution times:
```bash
GET /api/v1/admin/agents/{agent_id}/logs
```

## Maintenance Tasks

### Daily

- Monitor system health
- Check error logs
- Verify backups completed

### Weekly

- Review audit logs
- Clear expired cache
- Check storage usage

### Monthly

- Clean up old workflows
- Review user access
- Update documentation
- Review agent performance

### Quarterly

- Database vacuum/analyze
- Update dependencies
- Security audit
- Performance review

## Upgrading

### Application Upgrade

1. Backup database
2. Pull latest code
3. Update dependencies:
```bash
cd backend
pip install -r requirements.txt

cd ../frontend
npm install
```

4. Apply migrations (if any)
5. Restart services

### Database Schema Changes

1. Create migration file
2. Test in staging
3. Backup production
4. Apply migration
5. Verify success

## Support

### Logs

- Application: `backend/logs/app.log`
- Audit: `storage/audit_logs/YYYY/MM/`
- Workflows: `storage/workflows/`

### Diagnostic Commands

```bash
# Database status
psql -U reg_user -d regulatory_reporting -c "\dt"

# ChromaDB collections
python -c "from app.db.chroma_db import *; print(get_chroma_client().list_collections())"

# Storage usage
du -sh storage/*

# Active processes
ps aux | grep python
```

### Getting Help

- Technical support: support@nttdata.com
- Documentation: `/docs`
- GitHub issues: (repository URL)
