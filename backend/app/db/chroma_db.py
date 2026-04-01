"""ChromaDB client for vector storage and knowledge graph"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import Optional

from app.core.config import settings

# Global client instance
_client: Optional[chromadb.Client] = None


def get_chroma_client() -> chromadb.Client:
    """
    Get or create ChromaDB client singleton.

    Returns:
        chromadb.Client: ChromaDB client instance
    """
    global _client

    if _client is None:
        # Create persistent client
        _client = chromadb.Client(
            ChromaSettings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=str(settings.CHROMA_PATH),
                anonymized_telemetry=False,
            )
        )

    return _client


def get_collection(name: str, create_if_not_exists: bool = True):
    """
    Get or create a ChromaDB collection.

    Args:
        name: Collection name
        create_if_not_exists: Create collection if it doesn't exist

    Returns:
        Collection instance
    """
    client = get_chroma_client()

    if create_if_not_exists:
        return client.get_or_create_collection(name=name)
    else:
        return client.get_collection(name=name)


# Standard collection names
COLLECTIONS = {
    "documents": "regulatory_documents",
    "requirements": "regulatory_requirements",
    "code": "generated_code",
    "knowledge_graph": "knowledge_graph",
}
