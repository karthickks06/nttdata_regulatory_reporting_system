"""NetworkX graph analyzer for advanced graph analysis and centrality metrics"""

from typing import Dict, Any, List, Optional, Set
import networkx as nx
from datetime import datetime
import json


class NetworkXAnalyzer:
    """
    Graph analyzer using NetworkX for advanced graph analysis.

    Capabilities:
    - Centrality analysis (betweenness, closeness, pagerank)
    - Shortest path finding
    - Subgraph extraction
    - Graph traversal and pattern matching
    - Community detection
    - Network flow analysis
    """

    def __init__(self, graph: Optional[nx.DiGraph] = None):
        self.name = "NetworkXAnalyzer"
        self.graph = graph or nx.DiGraph()

    def load_graph(self, graph: nx.DiGraph):
        """Load graph for analysis"""
        self.graph = graph

    async def calculate_centrality(
        self,
        centrality_type: str = "betweenness"
    ) -> Dict[str, Any]:
        """
        Calculate node centrality metrics.

        Args:
            centrality_type: Type of centrality (betweenness, closeness, pagerank, degree)

        Returns:
            Centrality scores for all nodes
        """
        try:
            if centrality_type == "betweenness":
                centrality = nx.betweenness_centrality(self.graph)
            elif centrality_type == "closeness":
                centrality = nx.closeness_centrality(self.graph)
            elif centrality_type == "pagerank":
                centrality = nx.pagerank(self.graph)
            elif centrality_type == "degree":
                centrality = dict(self.graph.degree())
            else:
                raise ValueError(f"Unknown centrality type: {centrality_type}")

            # Sort by centrality value
            sorted_nodes = sorted(
                centrality.items(),
                key=lambda x: x[1],
                reverse=True
            )

            return {
                "success": True,
                "centrality_type": centrality_type,
                "scores": dict(sorted_nodes),
                "top_nodes": sorted_nodes[:10],
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "centrality_type": centrality_type
            }

    async def find_shortest_path(
        self,
        source: str,
        target: str,
        weight: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Find shortest path between two nodes.

        Args:
            source: Source node ID
            target: Target node ID
            weight: Edge weight attribute (optional)

        Returns:
            Shortest path and distance
        """
        try:
            if source not in self.graph:
                return {"success": False, "error": f"Source node {source} not found"}

            if target not in self.graph:
                return {"success": False, "error": f"Target node {target} not found"}

            # Find shortest path
            path = nx.shortest_path(self.graph, source, target, weight=weight)

            # Calculate path length
            if weight:
                length = nx.shortest_path_length(self.graph, source, target, weight=weight)
            else:
                length = len(path) - 1

            # Extract path edges with properties
            path_edges = []
            for i in range(len(path) - 1):
                edge_data = self.graph[path[i]][path[i + 1]]
                path_edges.append({
                    "source": path[i],
                    "target": path[i + 1],
                    "properties": dict(edge_data)
                })

            return {
                "success": True,
                "source": source,
                "target": target,
                "path": path,
                "path_length": length,
                "edges": path_edges
            }

        except nx.NetworkXNoPath:
            return {
                "success": False,
                "error": f"No path exists between {source} and {target}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def extract_subgraph(
        self,
        node_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Extract subgraph containing specified nodes.

        Args:
            node_ids: List of node IDs to include

        Returns:
            Subgraph data
        """
        try:
            # Filter existing nodes
            existing_nodes = [n for n in node_ids if n in self.graph]

            if not existing_nodes:
                return {
                    "success": False,
                    "error": "None of the specified nodes exist in graph"
                }

            # Extract subgraph
            subgraph = self.graph.subgraph(existing_nodes)

            # Get nodes and edges
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
                    "properties": dict(self.graph[source][target])
                })

            return {
                "success": True,
                "nodes": nodes,
                "edges": edges,
                "nodes_count": len(nodes),
                "edges_count": len(edges)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def find_connected_components(self) -> Dict[str, Any]:
        """
        Find weakly connected components in the graph.

        Returns:
            List of connected components
        """
        try:
            components = list(nx.weakly_connected_components(self.graph))

            # Sort by size
            components = sorted(components, key=len, reverse=True)

            component_data = []
            for idx, comp in enumerate(components):
                component_data.append({
                    "component_id": idx,
                    "size": len(comp),
                    "nodes": list(comp)[:50]  # First 50 nodes
                })

            return {
                "success": True,
                "components_count": len(components),
                "components": component_data,
                "largest_component_size": len(components[0]) if components else 0
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def detect_cycles(self) -> Dict[str, Any]:
        """
        Detect cycles in the graph.

        Returns:
            List of cycles found
        """
        try:
            cycles = list(nx.simple_cycles(self.graph))

            # Limit to prevent overwhelming response
            cycles = cycles[:100]

            return {
                "success": True,
                "cycles_count": len(cycles),
                "cycles": cycles,
                "has_cycles": len(cycles) > 0
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def find_neighbors(
        self,
        node_id: str,
        depth: int = 1,
        direction: str = "both"
    ) -> Dict[str, Any]:
        """
        Find neighbors of a node up to specified depth.

        Args:
            node_id: Node ID
            depth: Traversal depth
            direction: Direction of traversal (outgoing, incoming, both)

        Returns:
            Neighbors at each depth level
        """
        try:
            if node_id not in self.graph:
                return {
                    "success": False,
                    "error": f"Node {node_id} not found"
                }

            neighbors_by_depth = {}
            visited = {node_id}

            current_level = {node_id}

            for d in range(1, depth + 1):
                next_level = set()

                for node in current_level:
                    if direction in ("outgoing", "both"):
                        # Outgoing edges (successors)
                        next_level.update(self.graph.successors(node))

                    if direction in ("incoming", "both"):
                        # Incoming edges (predecessors)
                        next_level.update(self.graph.predecessors(node))

                # Remove already visited nodes
                next_level -= visited

                neighbors_by_depth[d] = list(next_level)
                visited.update(next_level)
                current_level = next_level

            return {
                "success": True,
                "node_id": node_id,
                "depth": depth,
                "neighbors_by_depth": neighbors_by_depth,
                "total_neighbors": len(visited) - 1
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def calculate_graph_metrics(self) -> Dict[str, Any]:
        """
        Calculate various graph metrics.

        Returns:
            Dictionary of graph metrics
        """
        try:
            metrics = {
                "nodes_count": self.graph.number_of_nodes(),
                "edges_count": self.graph.number_of_edges(),
                "density": nx.density(self.graph),
                "is_directed": self.graph.is_directed(),
                "is_weakly_connected": nx.is_weakly_connected(self.graph),
            }

            # Average clustering coefficient
            try:
                metrics["avg_clustering"] = nx.average_clustering(
                    self.graph.to_undirected()
                )
            except:
                metrics["avg_clustering"] = None

            # Diameter (for connected graphs)
            try:
                if nx.is_weakly_connected(self.graph):
                    metrics["diameter"] = nx.diameter(self.graph.to_undirected())
                else:
                    metrics["diameter"] = None
            except:
                metrics["diameter"] = None

            # Average degree
            if self.graph.number_of_nodes() > 0:
                degrees = dict(self.graph.degree())
                metrics["avg_degree"] = sum(degrees.values()) / len(degrees)
            else:
                metrics["avg_degree"] = 0

            return {
                "success": True,
                "metrics": metrics,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def export_graph(
        self,
        format: str = "json"
    ) -> Dict[str, Any]:
        """
        Export graph in specified format.

        Args:
            format: Export format (json, gexf, graphml)

        Returns:
            Serialized graph data
        """
        try:
            if format == "json":
                data = nx.node_link_data(self.graph)
                return {
                    "success": True,
                    "format": format,
                    "data": data
                }
            elif format == "gexf":
                # GEXF format (for Gephi)
                import io
                buffer = io.StringIO()
                nx.write_gexf(self.graph, buffer)
                return {
                    "success": True,
                    "format": format,
                    "data": buffer.getvalue()
                }
            elif format == "graphml":
                import io
                buffer = io.StringIO()
                nx.write_graphml(self.graph, buffer)
                return {
                    "success": True,
                    "format": format,
                    "data": buffer.getvalue()
                }
            else:
                return {
                    "success": False,
                    "error": f"Unsupported format: {format}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
