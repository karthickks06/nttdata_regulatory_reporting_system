"""GraphRAG persistence service for storing and retrieving knowledge graphs"""

from typing import Dict, Any, Optional
from pathlib import Path
import json
import pickle
import networkx as nx
from datetime import datetime

from app.core.config import settings


class GraphRAGStorageService:
    """Service for GraphRAG persistence and retrieval"""

    def __init__(self):
        self.graphrag_dir = settings.STORAGE_PATH / "graphrag"
        self.graphs_dir = self.graphrag_dir / "graphs"
        self.communities_dir = self.graphrag_dir / "communities"
        self.entities_dir = self.graphrag_dir / "entities"
        self.analysis_dir = self.graphrag_dir / "analysis"

        # Ensure directories exist
        for directory in [self.graphs_dir, self.communities_dir, self.entities_dir, self.analysis_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    async def save_graph(
        self,
        graph_id: str,
        graph: nx.DiGraph,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Save NetworkX graph to storage.

        Args:
            graph_id: Unique graph identifier
            graph: NetworkX graph
            metadata: Graph metadata

        Returns:
            Save result
        """
        try:
            # Save as pickle for Python
            pickle_path = self.graphs_dir / f"{graph_id}.gpickle"
            with open(pickle_path, 'wb') as f:
                pickle.dump(graph, f)

            # Save as JSON for portability
            json_path = self.graphs_dir / f"{graph_id}.json"
            graph_data = nx.node_link_data(graph)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(graph_data, f, indent=2)

            # Save metadata
            meta_path = self.graphs_dir / f"{graph_id}_metadata.json"
            meta_data = {
                "graph_id": graph_id,
                "nodes_count": graph.number_of_nodes(),
                "edges_count": graph.number_of_edges(),
                "saved_at": datetime.utcnow().isoformat(),
                **(metadata or {})
            }
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(meta_data, f, indent=2)

            return {
                "success": True,
                "graph_id": graph_id,
                "pickle_path": str(pickle_path),
                "json_path": str(json_path)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def load_graph(
        self,
        graph_id: str
    ) -> Optional[nx.DiGraph]:
        """
        Load NetworkX graph from storage.

        Args:
            graph_id: Graph identifier

        Returns:
            NetworkX graph or None
        """
        try:
            pickle_path = self.graphs_dir / f"{graph_id}.gpickle"

            if not pickle_path.exists():
                return None

            with open(pickle_path, 'rb') as f:
                graph = pickle.load(f)

            return graph

        except Exception:
            return None

    async def save_communities(
        self,
        graph_id: str,
        communities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Save community detection results"""
        try:
            file_path = self.communities_dir / f"{graph_id}_communities.json"

            data = {
                "graph_id": graph_id,
                "communities": communities,
                "saved_at": datetime.utcnow().isoformat()
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            return {
                "success": True,
                "file_path": str(file_path)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def load_communities(
        self,
        graph_id: str
    ) -> Optional[Dict[str, Any]]:
        """Load community detection results"""
        try:
            file_path = self.communities_dir / f"{graph_id}_communities.json"

            if not file_path.exists():
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return data.get("communities")

        except Exception:
            return None

    async def save_entities(
        self,
        graph_id: str,
        entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Save extracted entities"""
        try:
            file_path = self.entities_dir / f"{graph_id}_entities.json"

            data = {
                "graph_id": graph_id,
                "entities": entities,
                "saved_at": datetime.utcnow().isoformat()
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)

            return {
                "success": True,
                "file_path": str(file_path)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def load_entities(
        self,
        graph_id: str
    ) -> Optional[Dict[str, Any]]:
        """Load extracted entities"""
        try:
            file_path = self.entities_dir / f"{graph_id}_entities.json"

            if not file_path.exists():
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return data.get("entities")

        except Exception:
            return None

    async def save_analysis(
        self,
        graph_id: str,
        analysis_type: str,
        analysis_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Save graph analysis results"""
        try:
            file_path = self.analysis_dir / f"{graph_id}_{analysis_type}.json"

            data = {
                "graph_id": graph_id,
                "analysis_type": analysis_type,
                "data": analysis_data,
                "analyzed_at": datetime.utcnow().isoformat()
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)

            return {
                "success": True,
                "file_path": str(file_path)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def list_graphs(self) -> Dict[str, Any]:
        """List all stored graphs"""
        try:
            graphs = []

            for meta_file in self.graphs_dir.glob("*_metadata.json"):
                with open(meta_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    graphs.append(metadata)

            return {
                "success": True,
                "graphs": graphs,
                "count": len(graphs)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
