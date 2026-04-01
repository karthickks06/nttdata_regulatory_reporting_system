# Database Migrations

This directory contains manual SQL migration files for the regulatory reporting system.

## Migration Strategy

Since we're not using Alembic, all database migrations are handled manually through SQL files.

### Initial Setup

On first run, `app.py` automatically creates all tables using SQLAlchemy's `Base.metadata.create_all()`.

### Adding New Changes

When you need to modify the database schema:

1. **Update the SQLAlchemy model** in `app/models/`
2. **Generate a migration SQL file** with a descriptive name:
   ```
   migrations/002_add_column_to_users.sql
   migrations/003_create_notifications_table.sql
   ```
3. **Apply the migration** manually:
   ```bash
   psql -U postgres -d regulatory_reporting -f migrations/002_add_column_to_users.sql
   ```

### Migration Naming Convention

Format: `<number>_<description>.sql`

Examples:
- `001_initial_schema.sql` - Initial schema (auto-generated)
- `002_add_user_preferences.sql`
- `003_add_notification_system.sql`
- `004_add_indexes_for_performance.sql`

### Generating Initial Schema

To generate the initial schema SQL from models:

```bash
python scripts/generate_schema_sql.py
```

This creates `migrations/001_initial_schema.sql` from the current model definitions.

## Applied Migrations Log

Keep track of applied migrations below:

- [x] 001_initial_schema.sql - Initial database schema (auto-created by app.py)

## Best Practices

1. Always test migrations on a development database first
2. Create a backup before applying migrations to production
3. Make migrations reversible when possible (include DROP/ALTER statements)
4. Document the purpose of each migration
5. Keep migrations small and focused on a single change
