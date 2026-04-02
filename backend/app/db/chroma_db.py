"""ChromaDB client for vector storage and knowledge graph"""

import logging
import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions
from typing import Optional, List, Dict, Any

from app.core.config import settings

logger = logging.getLogger(__name__)

# Global client instance
_client: Optional[chromadb.Client] = None
_embedding_function = None


def get_embedding_function():
    """
    Get or create embedding function based on LLM provider configuration.

    Returns:
        Embedding function instance
    """
    global _embedding_function

    if _embedding_function is None:
        try:
            # Use Azure OpenAI if configured
            if settings.LLM_PROVIDER == "azure" and settings.AZURE_OPENAI_API_KEY:
                _embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=settings.AZURE_OPENAI_API_KEY,
                    api_base=settings.AZURE_OPENAI_ENDPOINT,
                    api_type="azure",
                    api_version=settings.AZURE_OPENAI_API_VERSION,
                    model_name=settings.AZURE_OPENAI_DEPLOYMENT
                )
                logger.info("Using Azure OpenAI embeddings")

            # Use OpenAI if configured
            elif settings.LLM_PROVIDER == "openai" and settings.OPENAI_API_KEY:
                _embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=settings.OPENAI_API_KEY,
                    model_name="text-embedding-3-small"
                )
                logger.info("Using OpenAI embeddings")

            # Fallback to sentence transformers (local, no API key needed)
            else:
                logger.warning("No LLM API key configured, using local sentence transformers")
                _embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
                logger.info("Using SentenceTransformer embeddings (local)")

        except Exception as e:
            logger.error(f"Failed to initialize embedding function: {e}")
            logger.warning("Falling back to local sentence transformers")
            _embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )

    return _embedding_function


def get_chroma_client() -> chromadb.Client:
    """
    Get or create ChromaDB client singleton.

    Returns:
        chromadb.Client: ChromaDB client instance
    """
    global _client

    if _client is None:
        try:
            # Create persistent client
            _client = chromadb.PersistentClient(
                path=str(settings.CHROMA_PATH),
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True,
                )
            )
            logger.info(f"ChromaDB client initialized at {settings.CHROMA_PATH}")
        except Exception as e:
            logger.error(f"Error initializing ChromaDB client: {e}")
            raise

    return _client


def get_collection(name: str, create_if_not_exists: bool = True, metadata: Optional[Dict] = None):
    """
    Get or create a ChromaDB collection.

    Args:
        name: Collection name
        create_if_not_exists: Create collection if it doesn't exist
        metadata: Optional metadata for the collection

    Returns:
        Collection instance
    """
    client = get_chroma_client()

    try:
        if create_if_not_exists:
            return client.get_or_create_collection(
                name=name,
                embedding_function=get_embedding_function(),
                metadata=metadata or {}
            )
        else:
            return client.get_collection(
                name=name,
                embedding_function=get_embedding_function()
            )
    except Exception as e:
        logger.error(f"Error getting collection '{name}': {e}")
        raise


def list_collections() -> List[str]:
    """
    List all collections in ChromaDB.

    Returns:
        List of collection names
    """
    try:
        client = get_chroma_client()
        collections = client.list_collections()
        return [col.name for col in collections]
    except Exception as e:
        logger.error(f"Error listing collections: {e}")
        return []


def delete_collection(name: str) -> bool:
    """
    Delete a ChromaDB collection.

    Args:
        name: Collection name

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        client = get_chroma_client()
        client.delete_collection(name=name)
        logger.info(f"Deleted collection '{name}'")
        return True
    except Exception as e:
        logger.error(f"Error deleting collection '{name}': {e}")
        return False


def reset_chroma() -> bool:
    """
    Reset ChromaDB - delete all collections.

    WARNING: This will delete all data in ChromaDB!

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        client = get_chroma_client()
        client.reset()
        logger.warning("ChromaDB has been reset - all collections deleted")
        return True
    except Exception as e:
        logger.error(f"Error resetting ChromaDB: {e}")
        return False


def get_collection_stats(name: str) -> Dict[str, Any]:
    """
    Get statistics for a collection.

    Args:
        name: Collection name

    Returns:
        dict: Collection statistics
    """
    try:
        collection = get_collection(name, create_if_not_exists=False)
        return {
            "name": collection.name,
            "count": collection.count(),
            "metadata": collection.metadata,
        }
    except Exception as e:
        logger.error(f"Error getting stats for collection '{name}': {e}")
        return {"error": str(e)}


def init_collections() -> None:
    """
    Initialize all standard collections.

    This should be called on application startup.
    """
    try:
        for key, collection_name in COLLECTIONS.items():
            get_collection(
                collection_name,
                create_if_not_exists=True,
                metadata={"type": key, "description": f"Collection for {key}"}
            )
            logger.info(f"Initialized collection: {collection_name}")
    except Exception as e:
        logger.error(f"Error initializing collections: {e}")
        raise


def check_chroma_health() -> Dict[str, Any]:
    """
    Check ChromaDB health and return status.

    Returns:
        dict: Health status information
    """
    try:
        client = get_chroma_client()
        collections = client.list_collections()

        return {
            "status": "healthy",
            "collections_count": len(collections),
            "collections": [col.name for col in collections],
            "path": str(settings.CHROMA_PATH),
        }
    except Exception as e:
        logger.error(f"ChromaDB health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
        }


# Standard collection names
COLLECTIONS = {
    "documents": "regulatory_documents",
    "requirements": "regulatory_requirements",
    "mappings": "data_mappings",
    "code": "generated_code",
    "reports": "regulatory_reports",
    "knowledge_graph": "knowledge_graph",
    "embeddings": "general_embeddings",
}


# Collection access helpers
def get_documents_collection():
    """Get regulatory documents collection."""
    return get_collection(COLLECTIONS["documents"])


def get_requirements_collection():
    """Get regulatory requirements collection."""
    return get_collection(COLLECTIONS["requirements"])


def get_mappings_collection():
    """Get data mappings collection."""
    return get_collection(COLLECTIONS["mappings"])


def get_code_collection():
    """Get generated code collection."""
    return get_collection(COLLECTIONS["code"])


def get_reports_collection():
    """Get regulatory reports collection."""
    return get_collection(COLLECTIONS["reports"])


def get_knowledge_graph_collection():
    """Get knowledge graph collection."""
    return get_collection(COLLECTIONS["knowledge_graph"])


def get_embeddings_collection():
    """Get general embeddings collection."""
    return get_collection(COLLECTIONS["embeddings"])
