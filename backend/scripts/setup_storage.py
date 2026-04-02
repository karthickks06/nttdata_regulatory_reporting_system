#!/usr/bin/env python3
"""Setup storage directory structure"""

from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings


def setup_storage():
    """Create all required storage directories"""

    storage_dirs = [
        # ChromaDB storage - vector database
        "chroma_data/collections",
        "chroma_data/indexes",

        # Document storage
        "documents/fca",
        "documents/pra",
        "documents/boe",
        "documents/other",

        # Report storage
        "reports/submissions",
        "reports/validation",
        "reports/drafts",
        "reports/approved",

        # Logs storage
        "logs/application",
        "logs/audit",
        "logs/agents",
        "logs/daily",

        # Audit log storage
        "audit_logs",

        # Generated code storage
        "generated_code/sql",
        "generated_code/python",
        "generated_code/tests",

        # GraphRAG storage
        "graphrag/graphs",
        "graphrag/communities",
        "graphrag/entities",
        "graphrag/analysis",

        # Embedding storage
        "embeddings/vectors",
        "embeddings/tiktoken_cache",
        "embeddings/indexes",

        # Workflow storage
        "workflows/definitions",
        "workflows/executions",
        "workflows/state",
        "workflows/history",

        # File metadata storage
        "files/uploads",
        "files/processed",
        "files/archived",

        # Cache storage
        "cache/api",
        "cache/embeddings",
        "cache/queries",

        # Backup storage
        "backups/daily",
        "backups/weekly",
        "backups/monthly",

        # Temporary storage
        "temp/uploads",
        "temp/processing",
        "temp/exports",
    ]

    base_path = Path(settings.STORAGE_PATH)

    for dir_path in storage_dirs:
        full_path = base_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)

    print(f"✅ Created {len(storage_dirs)} storage directories under {base_path}")


if __name__ == "__main__":
    setup_storage()
