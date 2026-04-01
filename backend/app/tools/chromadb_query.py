"""ChromaDB query helper functions"""

from typing import Dict, Any, List, Optional
from app.db.chroma_db import get_collection, COLLECTIONS


async def query_documents(
    query_text: str,
    n_results: int = 5,
    collection_name: str = "documents",
    where: Optional[Dict[str, Any]] = None,
    where_document: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Query documents from ChromaDB collection.

    Args:
        query_text: Query text
        n_results: Number of results to return
        collection_name: Collection name
        where: Metadata filter
        where_document: Document content filter

    Returns:
        Query results
    """
    try:
        collection = get_collection(COLLECTIONS.get(collection_name, collection_name))

        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where,
            where_document=where_document
        )

        return {
            "success": True,
            "query": query_text,
            "results": {
                "ids": results.get("ids", [[]])[0],
                "documents": results.get("documents", [[]])[0],
                "metadatas": results.get("metadatas", [[]])[0],
                "distances": results.get("distances", [[]])[0]
            },
            "count": len(results.get("ids", [[]])[0])
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query": query_text
        }


async def add_documents(
    ids: List[str],
    documents: List[str],
    metadatas: Optional[List[Dict[str, Any]]] = None,
    embeddings: Optional[List[List[float]]] = None,
    collection_name: str = "documents"
) -> Dict[str, Any]:
    """
    Add documents to ChromaDB collection.

    Args:
        ids: Document IDs
        documents: Document texts
        metadatas: Document metadata
        embeddings: Pre-computed embeddings
        collection_name: Collection name

    Returns:
        Add result
    """
    try:
        collection = get_collection(COLLECTIONS.get(collection_name, collection_name))

        if embeddings:
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings
            )
        else:
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

        return {
            "success": True,
            "collection": collection_name,
            "added_count": len(ids)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "collection": collection_name
        }


async def update_documents(
    ids: List[str],
    documents: Optional[List[str]] = None,
    metadatas: Optional[List[Dict[str, Any]]] = None,
    embeddings: Optional[List[List[float]]] = None,
    collection_name: str = "documents"
) -> Dict[str, Any]:
    """
    Update documents in ChromaDB collection.

    Args:
        ids: Document IDs to update
        documents: Updated document texts
        metadatas: Updated metadata
        embeddings: Updated embeddings
        collection_name: Collection name

    Returns:
        Update result
    """
    try:
        collection = get_collection(COLLECTIONS.get(collection_name, collection_name))

        collection.update(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

        return {
            "success": True,
            "collection": collection_name,
            "updated_count": len(ids)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "collection": collection_name
        }


async def delete_documents(
    ids: List[str],
    collection_name: str = "documents"
) -> Dict[str, Any]:
    """
    Delete documents from ChromaDB collection.

    Args:
        ids: Document IDs to delete
        collection_name: Collection name

    Returns:
        Delete result
    """
    try:
        collection = get_collection(COLLECTIONS.get(collection_name, collection_name))

        collection.delete(ids=ids)

        return {
            "success": True,
            "collection": collection_name,
            "deleted_count": len(ids)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "collection": collection_name
        }


async def get_documents_by_ids(
    ids: List[str],
    collection_name: str = "documents"
) -> Dict[str, Any]:
    """
    Get documents by IDs.

    Args:
        ids: Document IDs
        collection_name: Collection name

    Returns:
        Documents with metadata
    """
    try:
        collection = get_collection(COLLECTIONS.get(collection_name, collection_name))

        results = collection.get(ids=ids)

        return {
            "success": True,
            "documents": {
                "ids": results.get("ids", []),
                "documents": results.get("documents", []),
                "metadatas": results.get("metadatas", [])
            },
            "count": len(results.get("ids", []))
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "collection": collection_name
        }


async def count_documents(collection_name: str = "documents") -> int:
    """
    Count documents in collection.

    Args:
        collection_name: Collection name

    Returns:
        Document count
    """
    try:
        collection = get_collection(COLLECTIONS.get(collection_name, collection_name))
        return collection.count()
    except:
        return 0


async def search_by_metadata(
    where: Dict[str, Any],
    collection_name: str = "documents",
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search documents by metadata filter.

    Args:
        where: Metadata filter conditions
        collection_name: Collection name
        limit: Maximum results

    Returns:
        Filtered documents
    """
    try:
        collection = get_collection(COLLECTIONS.get(collection_name, collection_name))

        results = collection.get(
            where=where,
            limit=limit
        )

        return {
            "success": True,
            "results": {
                "ids": results.get("ids", []),
                "documents": results.get("documents", []),
                "metadatas": results.get("metadatas", [])
            },
            "count": len(results.get("ids", []))
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "collection": collection_name
        }
