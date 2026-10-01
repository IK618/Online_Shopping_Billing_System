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

    # Approximate geographic coordinates (x=Longitude, y=Latitude relative)
    CITY_COORDS = {
        "Bengaluru (Hub)": (50, 24),
        "Chennai": (62, 22),
        "Kochi": (44, 12),
        "Hyderabad": (55, 40),
        "Vijayawada": (66, 37),
        "Visakhapatnam": (74, 46),
        "Pune": (36, 43),
        "Mumbai": (30, 48),
        "Nagpur": (54, 56),
        "Bhopal": (49, 65),
        "Ahmedabad": (24, 63),
        "Bhubaneswar": (79, 56),
        "Kolkata": (86, 63),
        "Jaipur": (38, 75),
        "Delhi": (45, 83),
        "Lucknow": (61, 78),
        "Chandigarh": (42, 92),
    }

    def generate_route_plot(self, highlighted_path: List[str] = None):
        """
        Renders a polished Matplotlib visualization of the Indian logistics map.
        Uses geographically accurate node positions and highlights optimal route.
        """
        fig, ax = plt.subplots(figsize=(10, 7.5), facecolor="#ffffff")
        pos = self.CITY_COORDS

        # 1. Background Highway Grid
        nx.draw_networkx_edges(self.graph, pos, edge_color="#e2e8f0", width=2.0, ax=ax, alpha=0.9)

        # 2. Standard Distribution Nodes
        regular_nodes = [n for n in self.graph.nodes() if n != CENTRAL_WAREHOUSE and (not highlighted_path or n not in highlighted_path)]
        nx.draw_networkx_nodes(self.graph, pos, nodelist=regular_nodes, node_color="#f1f5f9",
                               node_size=850, edgecolors="#cbd5e1", linewidths=1.5, ax=ax)
        nx.draw_networkx_labels(self.graph, pos, labels={n: n for n in regular_nodes},
                                font_size=8.5, font_family="sans-serif", font_color="#475569", font_weight="600", ax=ax)

        # 3. Central Hub (Bengaluru) with prominent gold halo
        nx.draw_networkx_nodes(self.graph, pos, nodelist=[CENTRAL_WAREHOUSE], node_color="#f59e0b",
                               node_size=1500, edgecolors="#d97706", linewidths=2.5, ax=ax)
        nx.draw_networkx_labels(self.graph, pos, labels={CENTRAL_WAREHOUSE: "Bengaluru\n(Central Hub)"},
                                font_size=8.5, font_family="sans-serif", font_color="#ffffff", font_weight="bold", ax=ax)

        # 4. Highlighted Optimal Route (Vibrant Emerald Green)
        if highlighted_path and len(highlighted_path) > 1:
            path_edges = list(zip(highlighted_path[:-1], highlighted_path[1:]))
            transit_nodes = [n for n in highlighted_path if n != CENTRAL_WAREHOUSE]
            
            # Glowing edge line
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, edge_color="#10b981", width=4.5, ax=ax, alpha=0.95)
            nx.draw_networkx_nodes(self.graph, pos, nodelist=transit_nodes, node_color="#10b981",
                                   node_size=1000, edgecolors="#047857", linewidths=2.0, ax=ax)
            nx.draw_networkx_labels(self.graph, pos, labels={n: n for n in transit_nodes},
                                    font_size=9, font_family="sans-serif", font_color="#ffffff", font_weight="bold", ax=ax)

        # Edge distance labels along active route or key highways
        edge_labels = {(u, v): f"{d['weight']} km" for u, v, d in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=7, font_color="#94a3b8", ax=ax)

        dest_name = highlighted_path[-1] if highlighted_path else "All Destinations"
        ax.set_title(f"📍 SmartCart India Dispatch Network — Active Corridor to [{dest_name}]",
                     fontsize=12, fontweight="bold", pad=14, color="#0f172a")
        ax.axis("off")
        fig.tight_layout()
        return fig
