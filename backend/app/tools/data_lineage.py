"""Data lineage tracking utilities"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import networkx as nx


class DataLineageTracker:
    """
    Track data lineage and transformations.

    Tracks data flow from source to destination through transformations.
    """

    def __init__(self):
        self.lineage_graph = nx.DiGraph()

    def add_data_source(
        self,
        source_id: str,
        source_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add a data source node.

        Args:
            source_id: Source identifier
            source_type: Type of source (table, file, api, etc.)
            metadata: Additional metadata

        Returns:
            Operation result
        """
        try:
            self.lineage_graph.add_node(
                source_id,
                node_type="source",
                source_type=source_type,
                created_at=datetime.utcnow().isoformat(),
                **(metadata or {})
            )

            return {
                "success": True,
                "source_id": source_id
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def add_transformation(
        self,
        transformation_id: str,
        transformation_type: str,
        description: Optional[str] = None,
        code: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add a transformation node.

        Args:
            transformation_id: Transformation identifier
            transformation_type: Type (sql, python, etc.)
            description: Transformation description
            code: Transformation code
            metadata: Additional metadata

        Returns:
            Operation result
        """
        try:
            self.lineage_graph.add_node(
                transformation_id,
                node_type="transformation",
                transformation_type=transformation_type,
                description=description,
                code=code,
                created_at=datetime.utcnow().isoformat(),
                **(metadata or {})
            )

            return {
                "success": True,
                "transformation_id": transformation_id
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def add_data_target(
        self,
        target_id: str,
        target_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add a data target node.

        Args:
            target_id: Target identifier
            target_type: Type of target (table, file, report, etc.)
            metadata: Additional metadata

        Returns:
            Operation result
        """
        try:
            self.lineage_graph.add_node(
                target_id,
                node_type="target",
                target_type=target_type,
                created_at=datetime.utcnow().isoformat(),
                **(metadata or {})
            )

            return {
                "success": True,
                "target_id": target_id
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def add_lineage_edge(
        self,
        from_id: str,
        to_id: str,
        relationship: str = "transforms_to",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add edge representing data flow.

        Args:
            from_id: Source node ID
            to_id: Target node ID
            relationship: Type of relationship
            metadata: Additional metadata

        Returns:
            Operation result
        """
        try:
            if from_id not in self.lineage_graph:
                return {
                    "success": False,
                    "error": f"Source node {from_id} not found"
                }

            if to_id not in self.lineage_graph:
                return {
                    "success": False,
                    "error": f"Target node {to_id} not found"
                }

            self.lineage_graph.add_edge(
                from_id,
                to_id,
                relationship=relationship,
                created_at=datetime.utcnow().isoformat(),
                **(metadata or {})
            )

            return {
                "success": True,
                "from": from_id,
                "to": to_id
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_upstream_lineage(
        self,
        node_id: str,
        max_depth: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get upstream lineage (sources) for a node.

        Args:
            node_id: Node identifier
            max_depth: Maximum traversal depth

        Returns:
            Upstream lineage data
        """
        try:
            if node_id not in self.lineage_graph:
                return {
                    "success": False,
                    "error": f"Node {node_id} not found"
                }

            # Get all predecessors (upstream)
            if max_depth:
                # BFS with depth limit
                upstream_nodes = set()
                queue = [(node_id, 0)]
                visited = {node_id}

                while queue:
                    current, depth = queue.pop(0)

                    if depth < max_depth:
                        for pred in self.lineage_graph.predecessors(current):
                            if pred not in visited:
                                visited.add(pred)
                                upstream_nodes.add(pred)
                                queue.append((pred, depth + 1))
            else:
                upstream_nodes = nx.ancestors(self.lineage_graph, node_id)

            # Build lineage paths
            nodes = []
            edges = []

            for node in upstream_nodes:
                nodes.append({
                    "id": node,
                    "data": dict(self.lineage_graph.nodes[node])
                })

            # Get edges in upstream subgraph
            upstream_nodes.add(node_id)
            subgraph = self.lineage_graph.subgraph(upstream_nodes)

            for source, target in subgraph.edges():
                edges.append({
                    "from": source,
                    "to": target,
                    "data": dict(self.lineage_graph[source][target])
                })

            return {
                "success": True,
                "node_id": node_id,
                "nodes": nodes,
                "edges": edges,
                "count": len(nodes)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_downstream_lineage(
        self,
        node_id: str,
        max_depth: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get downstream lineage (targets) for a node.

        Args:
            node_id: Node identifier
            max_depth: Maximum traversal depth

        Returns:
            Downstream lineage data
        """
        try:
            if node_id not in self.lineage_graph:
                return {
                    "success": False,
                    "error": f"Node {node_id} not found"
                }

            # Get all successors (downstream)
            if max_depth:
                downstream_nodes = set()
                queue = [(node_id, 0)]
                visited = {node_id}

                while queue:
                    current, depth = queue.pop(0)

                    if depth < max_depth:
                        for succ in self.lineage_graph.successors(current):
                            if succ not in visited:
                                visited.add(succ)
                                downstream_nodes.add(succ)
                                queue.append((succ, depth + 1))
            else:
                downstream_nodes = nx.descendants(self.lineage_graph, node_id)

            # Build lineage data
            nodes = []
            edges = []

            for node in downstream_nodes:
                nodes.append({
                    "id": node,
                    "data": dict(self.lineage_graph.nodes[node])
                })

            # Get edges
            downstream_nodes.add(node_id)
            subgraph = self.lineage_graph.subgraph(downstream_nodes)

            for source, target in subgraph.edges():
                edges.append({
                    "from": source,
                    "to": target,
                    "data": dict(self.lineage_graph[source][target])
                })

            return {
                "success": True,
                "node_id": node_id,
                "nodes": nodes,
                "edges": edges,
                "count": len(nodes)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_full_lineage(
        self,
        node_id: str
    ) -> Dict[str, Any]:
        """
        Get complete lineage (upstream and downstream) for a node.

        Args:
            node_id: Node identifier

        Returns:
            Complete lineage data
        """
        try:
            upstream = self.get_upstream_lineage(node_id)
            downstream = self.get_downstream_lineage(node_id)

            if not upstream["success"] or not downstream["success"]:
                return {
                    "success": False,
                    "error": "Failed to retrieve lineage"
                }

            # Combine nodes and edges
            all_nodes = upstream["nodes"] + downstream["nodes"]
            all_edges = upstream["edges"] + downstream["edges"]

            # Add the central node
            all_nodes.append({
                "id": node_id,
                "data": dict(self.lineage_graph.nodes[node_id])
            })

            # Remove duplicates
            unique_nodes = {node["id"]: node for node in all_nodes}
            unique_edges = {(edge["from"], edge["to"]): edge for edge in all_edges}

            return {
                "success": True,
                "node_id": node_id,
                "nodes": list(unique_nodes.values()),
                "edges": list(unique_edges.values()),
                "upstream_count": upstream["count"],
                "downstream_count": downstream["count"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def find_impact_analysis(
        self,
        source_id: str
    ) -> Dict[str, Any]:
        """
        Find all targets impacted by a source change.

        Args:
            source_id: Source node identifier

        Returns:
            Impact analysis results
        """
        return self.get_downstream_lineage(source_id)

    def find_source_of_truth(
        self,
        target_id: str
    ) -> Dict[str, Any]:
        """
        Find original sources for a target.

        Args:
            target_id: Target node identifier

        Returns:
            Source of truth nodes
        """
        upstream = self.get_upstream_lineage(target_id)

        if not upstream["success"]:
            return upstream

        # Filter for source nodes only
        sources = [
            node for node in upstream["nodes"]
            if node["data"].get("node_type") == "source"
        ]

        return {
            "success": True,
            "target_id": target_id,
            "sources": sources,
            "count": len(sources)
        }

    def export_lineage(self) -> Dict[str, Any]:
        """
        Export complete lineage graph.

        Returns:
            Graph export data
        """
        try:
            nodes = []
            for node_id in self.lineage_graph.nodes():
                nodes.append({
                    "id": node_id,
                    "data": dict(self.lineage_graph.nodes[node_id])
                })

            edges = []
            for source, target in self.lineage_graph.edges():
                edges.append({
                    "from": source,
                    "to": target,
                    "data": dict(self.lineage_graph[source][target])
                })

            return {
                "success": True,
                "nodes": nodes,
                "edges": edges,
                "node_count": len(nodes),
                "edge_count": len(edges)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
