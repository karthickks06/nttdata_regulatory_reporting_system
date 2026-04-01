#!/usr/bin/env python3
"""Generate SQL schema from SQLAlchemy models"""

import sys
from pathlib import Path
from io import StringIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.postgres import Base
from app.models import (
    user, role, permission, session, cache, rate_limit,
    task_queue, regulatory_update, requirement, data_mapping,
    generated_code, test_case, report, workflow,
    file_metadata, audit_log
)
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql


def generate_schema_sql():
    """Generate SQL CREATE TABLE statements from models"""

    output = StringIO()
    output.write("-- Generated SQL Schema\n")
    output.write("-- Auto-generated from SQLAlchemy models\n")
    output.write(f"-- Generated at: {__import__('datetime').datetime.now()}\n\n")

    # Generate CREATE TABLE statements
    for table in Base.metadata.sorted_tables:
        create_stmt = CreateTable(table).compile(dialect=postgresql.dialect())
        output.write(f"{create_stmt};\n\n")

    sql_content = output.getvalue()

    # Write to file
    migrations_dir = Path(__file__).parent.parent / "migrations"
    migrations_dir.mkdir(exist_ok=True)

    output_file = migrations_dir / "001_initial_schema.sql"
    output_file.write_text(sql_content)

    print(f"✅ Generated SQL schema: {output_file}")
    print(f"   Total tables: {len(Base.metadata.tables)}")


if __name__ == "__main__":
    generate_schema_sql()
