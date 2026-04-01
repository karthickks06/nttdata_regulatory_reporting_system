"""ChromaDB + GraphRAG unified agent for knowledge graph and vector storage"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import networkx as nx

from app.db.chroma_db import get_collection, COLLECTIONS
from app.core.config import settings


class ChromaDBGraphRAGAgent:
    """
    Unified agent for ChromaDB vector storage and GraphRAG knowledge graph.

    Capabilities:
    - Store and query document embeddings in ChromaDB
    - Build knowledge graphs from entities and relationships
    - Perform vector similarity search
    - Query knowledge graph for entity relationships
    - Community detection and graph analysis
    """

    def __init__(self):
        self.name = "ChromaDBGraphRAG"
        self.document_collection = None
        self.knowledge_graph_collection = None
        self.graph = nx.DiGraph()

    async def initialize(self):
        """Initialize ChromaDB collections"""
        self.document_collection = get_collection(COLLECTIONS["documents"])
        self.knowledge_graph_collection = get_collection(COLLECTIONS["knowledge_graph"])

    async def store_document_embeddings(
        self,
        document_id: str,
        text_chunks: List[str],
        metadatas: List[Dict[str, Any]],
        embeddings: Optional[List[List[float]]] = None
    ) -> Dict[str, Any]:
        """
        Store document embeddings in ChromaDB.

        Args:
            document_id: Unique document identifier
            text_chunks: List of text chunks
            metadatas: Metadata for each chunk
            embeddings: Pre-computed embeddings (optional)

        Returns:
            Storage result with IDs
        """
        try:
            # Generate IDs for chunks
            chunk_ids = [f"{document_id}_chunk_{i}" for i in range(len(text_chunks))]

            # Store in ChromaDB
            if embeddings:
                self.document_collection.add(
                    ids=chunk_ids,
                    documents=text_chunks,
                    metadatas=metadatas,
                    embeddings=embeddings
                )
            else:
                # Let ChromaDB generate embeddings
                self.document_collection.add(
                    ids=chunk_ids,
                    documents=text_chunks,
                    metadatas=metadatas
                )

            return {
                "success": True,
                "document_id": document_id,
                "chunks_stored": len(text_chunks),
                "chunk_ids": chunk_ids,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "document_id": document_id
            }

    async def query_documents(
        self,
        query_text: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query documents using vector similarity search.

        Args:
            query_text: Query text
            n_results: Number of results to return
            where: Metadata filter

        Returns:
            Query results with documents and scores
        """
        try:
            results = self.document_collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where
            )

            return {
                "success": True,
                "query": query_text,
                "results": {
                    "documents": results["documents"][0] if results["documents"] else [],
                    "metadatas": results["metadatas"][0] if results["metadatas"] else [],
                    "distances": results["distances"][0] if results["distances"] else [],
                    "ids": results["ids"][0] if results["ids"] else []
                },
                "count": len(results["ids"][0]) if results["ids"] else 0
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "query": query_text
            }

    async def build_knowledge_graph(
        self,
        entities: List[Dict[str, Any]],
        relationships: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Build knowledge graph from entities and relationships.

        Args:
            entities: List of entities with properties
            relationships: List of relationships between entities

        Returns:
            Graph building result
        """
        try:
            # Add entities as nodes
            for entity in entities:
                entity_id = entity.get("id")
                entity_type = entity.get("type")
                properties = entity.get("properties", {})

                self.graph.add_node(
                    entity_id,
                    type=entity_type,
                    **properties
                )

            # Add relationships as edges
            for rel in relationships:
                source = rel.get("source")
                target = rel.get("target")
                rel_type = rel.get("type")
                properties = rel.get("properties", {})

                self.graph.add_edge(
                    source,
                    target,
                    type=rel_type,
                    **properties
                )

            # Store graph metadata in ChromaDB
            await self._store_graph_metadata()

            return {
                "success": True,
                "nodes_count": self.graph.number_of_nodes(),
                "edges_count": self.graph.number_of_edges(),
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _store_graph_metadata(self):
        """Store graph structure metadata in ChromaDB"""
        # Store each node as a document with its properties
        node_docs = []
        node_metas = []
        node_ids = []

        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]

            # Create document text
            doc_text = f"Entity: {node_id}, Type: {node_data.get('type', 'Unknown')}"

            # Get connected nodes
            neighbors = list(self.graph.neighbors(node_id))

            metadata = {
                "entity_id": node_id,
                "entity_type": node_data.get('type', 'Unknown'),
                "neighbors": json.dumps(neighbors[:10]),  # Store first 10 neighbors
                "degree": self.graph.degree(node_id),
                "stored_at": datetime.utcnow().isoformat()
            }

            node_docs.append(doc_text)
            node_metas.append(metadata)
            node_ids.append(f"node_{node_id}")

        # Store in ChromaDB
        if node_docs:
            self.knowledge_graph_collection.add(
                ids=node_ids,
                documents=node_docs,
                metadatas=node_metas
            )

    async def query_knowledge_graph(
        self,
        entity_id: str,
        relationship_type: Optional[str] = None,
        max_depth: int = 2
    ) -> Dict[str, Any]:
        """
        Query knowledge graph for entity relationships.

        Args:
            entity_id: Starting entity ID
            relationship_type: Filter by relationship type
            max_depth: Maximum traversal depth

        Returns:
            Subgraph with related entities
        """
        try:
            if entity_id not in self.graph:
                return {
                    "success": False,
                    "error": f"Entity {entity_id} not found in graph"
                }

            # Get subgraph within max_depth
            subgraph_nodes = nx.single_source_shortest_path_length(
                self.graph,
                entity_id,
                cutoff=max_depth
            )

            subgraph = self.graph.subgraph(subgraph_nodes.keys())

            # Extract nodes and edges
            nodes = []
            for node in subgraph.nodes():
                nodes.append({
                    "id": node,
                    "properties": dict(self.graph.nodes[node])
                })

            edges = []
            for source, target in subgraph.edges():
                edges.append({
                    "source": source,
                    "target": target,
                    "type": self.graph[source][target].get("type"),
                    "properties": dict(self.graph[source][target])
                })

            return {
                "success": True,
                "entity_id": entity_id,
                "nodes": nodes,
                "edges": edges,
                "nodes_count": len(nodes),
                "edges_count": len(edges)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "entity_id": entity_id
            }

    async def find_communities(self) -> Dict[str, Any]:
        """
        Detect communities in the knowledge graph.

        Returns:
            Community detection results
        """
        try:
            from networkx.algorithms import community

            # Convert to undirected for community detection
            undirected_graph = self.graph.to_undirected()

            # Detect communities using Louvain method
            communities = community.louvain_communities(undirected_graph)

            # Format results
            community_data = []
            for idx, comm in enumerate(communities):
                community_data.append({
                    "community_id": idx,
                    "size": len(comm),
                    "members": list(comm)[:20]  # First 20 members
                })

            return {
                "success": True,
                "communities_count": len(communities),
                "communities": community_data,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def get_graph_statistics(self) -> Dict[str, Any]:
        """
        Get knowledge graph statistics.

        Returns:
            Graph statistics and metrics
        """
        try:
            stats = {
                "nodes_count": self.graph.number_of_nodes(),
                "edges_count": self.graph.number_of_edges(),
                "density": nx.density(self.graph),
                "is_connected": nx.is_weakly_connected(self.graph),
                "avg_degree": sum(dict(self.graph.degree()).values()) / max(self.graph.number_of_nodes(), 1)
            }

            # Node type distribution
            node_types = {}
            for node in self.graph.nodes():
                node_type = self.graph.nodes[node].get("type", "Unknown")
                node_types[node_type] = node_types.get(node_type, 0) + 1

            stats["node_types"] = node_types

            return {
                "success": True,
                "statistics": stats,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
