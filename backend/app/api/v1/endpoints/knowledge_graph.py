"""
Knowledge Graph API Endpoints - ChromaDB and GraphRAG queries
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.sub_agents.chromadb_graph_rag_agent import ChromaDBGraphRAGAgent
from app.sub_agents.networkx_analyzer import NetworkXAnalyzer
from app.core.rbac import require_permission

router = APIRouter()


@router.post("/search")
async def search_knowledge_graph(
    query: str,
    top_k: int = 10,
    filter_metadata: Optional[Dict[str, Any]] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search the knowledge graph using semantic search"""
    await require_permission(db, current_user.id, "knowledge_graph", "read")

    agent = ChromaDBGraphRAGAgent()

    try:
        results = await agent.search(
            query=query,
            top_k=top_k,
            filter_metadata=filter_metadata
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.post("/entities/add")
async def add_entity(
    entity_type: str,
    entity_id: str,
    description: str,
    metadata: Optional[Dict[str, Any]] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add an entity to the knowledge graph"""
    await require_permission(db, current_user.id, "knowledge_graph", "create")

    agent = ChromaDBGraphRAGAgent()

    try:
        result = await agent.add_entity(
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            metadata=metadata or {}
        )
        return {"status": "success", "entity_id": entity_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add entity: {str(e)}"
        )


@router.post("/relationships/add")
async def add_relationship(
    source_id: str,
    target_id: str,
    relationship_type: str,
    metadata: Optional[Dict[str, Any]] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a relationship between entities"""
    await require_permission(db, current_user.id, "knowledge_graph", "create")

    agent = ChromaDBGraphRAGAgent()

    try:
        result = await agent.add_relationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            metadata=metadata or {}
        )
        return {"status": "success", "relationship": relationship_type}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add relationship: {str(e)}"
        )


@router.get("/entities/{entity_id}")
async def get_entity(
    entity_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get entity details from knowledge graph"""
    await require_permission(db, current_user.id, "knowledge_graph", "read")

    agent = ChromaDBGraphRAGAgent()

    try:
        entity = await agent.get_entity(entity_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found"
            )
        return entity
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve entity: {str(e)}"
        )


@router.get("/entities/{entity_id}/relationships")
async def get_entity_relationships(
    entity_id: str,
    relationship_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all relationships for an entity"""
    await require_permission(db, current_user.id, "knowledge_graph", "read")

    agent = ChromaDBGraphRAGAgent()

    try:
        relationships = await agent.get_entity_relationships(
            entity_id=entity_id,
            relationship_type=relationship_type
        )
        return relationships
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve relationships: {str(e)}"
        )


@router.get("/graph/communities")
async def get_communities(
    min_size: int = 3,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get community detection results"""
    await require_permission(db, current_user.id, "knowledge_graph", "read")

    analyzer = NetworkXAnalyzer()

    try:
        communities = await analyzer.detect_communities(min_size=min_size)
        return communities
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Community detection failed: {str(e)}"
        )


@router.get("/graph/centrality")
async def calculate_centrality(
    metric: str = "betweenness",
    top_k: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate centrality metrics for graph nodes"""
    await require_permission(db, current_user.id, "knowledge_graph", "read")

    analyzer = NetworkXAnalyzer()

    valid_metrics = ["betweenness", "degree", "closeness", "eigenvector"]
    if metric not in valid_metrics:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid metric. Must be one of: {valid_metrics}"
        )

    try:
        centrality = await analyzer.calculate_centrality(
            metric=metric,
            top_k=top_k
        )
        return centrality
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Centrality calculation failed: {str(e)}"
        )


@router.get("/graph/path/{source_id}/{target_id}")
async def find_shortest_path(
    source_id: str,
    target_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Find shortest path between two entities"""
    await require_permission(db, current_user.id, "knowledge_graph", "read")

    analyzer = NetworkXAnalyzer()

    try:
        path = await analyzer.find_shortest_path(
            source_id=source_id,
            target_id=target_id
        )
        return path
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Path finding failed: {str(e)}"
        )


@router.get("/graph/subgraph/{entity_id}")
async def get_subgraph(
    entity_id: str,
    depth: int = 2,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get subgraph around an entity"""
    await require_permission(db, current_user.id, "knowledge_graph", "read")

    analyzer = NetworkXAnalyzer()

    try:
        subgraph = await analyzer.get_subgraph(
            entity_id=entity_id,
            depth=depth
        )
        return subgraph
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Subgraph extraction failed: {str(e)}"
        )


@router.get("/graph/statistics")
async def get_graph_statistics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get overall graph statistics"""
    await require_permission(db, current_user.id, "knowledge_graph", "read")

    analyzer = NetworkXAnalyzer()

    try:
        stats = await analyzer.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve statistics: {str(e)}"
        )


@router.post("/graph/rebuild")
async def rebuild_graph(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Rebuild the knowledge graph from ChromaDB"""
    await require_permission(db, current_user.id, "knowledge_graph", "admin")

    agent = ChromaDBGraphRAGAgent()

    try:
        result = await agent.rebuild_graph()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Graph rebuild failed: {str(e)}"
        )
