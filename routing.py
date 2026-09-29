"""
routing.py
Logistics & Delivery Route Optimization Engine
Demonstrates:
  - Session 10: NetworkX (Graph, add_node, add_edge, draw_networkx)
  - Session 10: SciPy Graph Processing (scipy.sparse.csgraph.dijkstra, Adjacency Matrix)
  - Session 10: Matplotlib (Network visualization, node colors, edge weights)
"""

import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict

# Central Distribution Warehouse
CENTRAL_WAREHOUSE = "Bengaluru (Hub)"

# Delivery Network Map: Hubs and delivery corridors with distances in km
CITY_CONNECTIONS = [
    ("Bengaluru (Hub)", "Chennai", 346),
    ("Bengaluru (Hub)", "Hyderabad", 569),
    ("Bengaluru (Hub)", "Kochi", 548),
    ("Chennai", "Vijayawada", 450),
    ("Hyderabad", "Vijayawada", 274),
    ("Hyderabad", "Nagpur", 500),
    ("Vijayawada", "Visakhapatnam", 350),
    ("Visakhapatnam", "Bhubaneswar", 440),
    ("Nagpur", "Bhopal", 350),
    ("Nagpur", "Kolkata", 980),
    ("Bhopal", "Mumbai", 770),
    ("Bhopal", "Delhi", 750),
    ("Mumbai", "Ahmedabad", 525),
    ("Mumbai", "Pune", 150),
    ("Pune", "Bengaluru (Hub)", 840),
    ("Ahmedabad", "Jaipur", 660),
    ("Jaipur", "Delhi", 280),
    ("Delhi", "Chandigarh", 250),
    ("Delhi", "Lucknow", 550),
    ("Lucknow", "Kolkata", 985),
    ("Bhubaneswar", "Kolkata", 440),
]


class LogisticsOptimizer:
    """Optimizes supply-chain shipping paths across Indian metropolitan delivery hubs."""

    def __init__(self):
        self.graph = nx.Graph()
        self._build_graph()

    def _build_graph(self):
        """Constructs NetworkX graph with weighted distance edges."""
        for u, v, dist in CITY_CONNECTIONS:
            self.graph.add_edge(u, v, weight=dist)

    def get_all_cities(self) -> List[str]:
        """Returns sorted list of delivery destination cities."""
        return sorted([node for node in self.graph.nodes() if node != CENTRAL_WAREHOUSE])

    def find_shortest_route(self, destination: str) -> Tuple[List[str], float]:
        """
        Calculates shortest path using both NetworkX and SciPy Dijkstra.
        Demonstrates: scipy.sparse.csgraph.dijkstra on adjacency matrix.
        """
        if destination not in self.graph:
            return ([CENTRAL_WAREHOUSE, destination], 0.0)

        # 1. NetworkX shortest path
        nx_path = nx.shortest_path(self.graph, source=CENTRAL_WAREHOUSE, target=destination, weight="weight")
        nx_dist = nx.shortest_path_length(self.graph, source=CENTRAL_WAREHOUSE, target=destination, weight="weight")

        # 2. SciPy Dijkstra verification using Adjacency Matrix (Session 10)
        nodes = list(self.graph.nodes())
        node_to_idx = {node: i for i, node in enumerate(nodes)}
        
        # Build SciPy sparse adjacency matrix
        adj_matrix = nx.to_scipy_sparse_array(self.graph, nodelist=nodes, weight="weight")
        dist_matrix, predecessors = dijkstra(
            csgraph=adj_matrix,
            directed=False,
            indices=node_to_idx[CENTRAL_WAREHOUSE],
            return_predecessors=True
        )

        scipy_dist = dist_matrix[node_to_idx[destination]]
        return nx_path, float(scipy_dist)

    def generate_route_plot(self, highlighted_path: List[str] = None):
        """
        Renders a Matplotlib visualization of the distribution graph.
        Highlights the computed delivery route in bold green.
        """
        fig, ax = plt.subplots(figsize=(10, 7), facecolor="#f8f9fa")
        pos = nx.spring_layout(self.graph, seed=42, k=1.2)

        # Default nodes & edges
        nx.draw_networkx_nodes(self.graph, pos, node_color="#cbd5e1", node_size=800, ax=ax)
        nx.draw_networkx_edges(self.graph, pos, edge_color="#94a3b8", width=1.5, ax=ax)
        nx.draw_networkx_labels(self.graph, pos, font_size=9, font_family="sans-serif", font_weight="bold", ax=ax)

        # Highlight central hub in gold
        nx.draw_networkx_nodes(self.graph, pos, nodelist=[CENTRAL_WAREHOUSE], node_color="#f59e0b", node_size=1200, ax=ax)

        # Highlight optimal delivery path if provided
        if highlighted_path and len(highlighted_path) > 1:
            path_edges = list(zip(highlighted_path[:-1], highlighted_path[1:]))
            nx.draw_networkx_nodes(self.graph, pos, nodelist=highlighted_path, node_color="#10b981", node_size=900, ax=ax)
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, edge_color="#059669", width=4.0, ax=ax)

        # Edge distance labels
        edge_labels = {(u, v): f"{d['weight']} km" for u, v, d in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=7, font_color="#64748b", ax=ax)

        dest_name = highlighted_path[-1] if highlighted_path else "All Hubs"
        ax.set_title(f"SmartCart Logistics Network - Optimal Dispatch Route to [{dest_name}]",
                     fontsize=12, fontweight="bold", pad=12, color="#1e293b")
        ax.axis("off")
        fig.tight_layout()
        return fig
