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
        Renders a polished dark-slate Matplotlib visualization inspired by Haulix Logistics.
        Uses geographically accurate node positions with glowing neon transit corridors.
        """
        fig, ax = plt.subplots(figsize=(10, 7.5), facecolor="#0B0F19")
        ax.set_facecolor("#0B0F19")
        pos = self.CITY_COORDS

        # 1. Subtle Background Highway Grid (Dark slate links)
        nx.draw_networkx_edges(self.graph, pos, edge_color="#1E293B", width=2.0, ax=ax, alpha=0.9)

        # 2. Standard Regional Distribution Nodes
        regular_nodes = [n for n in self.graph.nodes() if n != CENTRAL_WAREHOUSE and (not highlighted_path or n not in highlighted_path)]
        nx.draw_networkx_nodes(self.graph, pos, nodelist=regular_nodes, node_color="#131C2E",
                               node_size=850, edgecolors="#2A384F", linewidths=1.5, ax=ax)
        nx.draw_networkx_labels(self.graph, pos, labels={n: n for n in regular_nodes},
                                font_size=8.5, font_family="sans-serif", font_color="#94A3B8", font_weight="600", ax=ax)

        # 3. Central Fulfillment Center (Bengaluru) with vibrant golden amber core
        nx.draw_networkx_nodes(self.graph, pos, nodelist=[CENTRAL_WAREHOUSE], node_color="#F59E0B",
                               node_size=1550, edgecolors="#D97706", linewidths=3.0, ax=ax)
        nx.draw_networkx_labels(self.graph, pos, labels={CENTRAL_WAREHOUSE: "Bengaluru\n(Hub)"},
                                font_size=8.5, font_family="sans-serif", font_color="#000000", font_weight="bold", ax=ax)

        # 4. Highlighted Optimal Route (Haulix Glowing Emerald Neon)
        if highlighted_path and len(highlighted_path) > 1:
            path_edges = list(zip(highlighted_path[:-1], highlighted_path[1:]))
            transit_nodes = [n for n in highlighted_path if n != CENTRAL_WAREHOUSE]
            
            # Thick Neon Corridor Glow
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, edge_color="#064E3B", width=7.0, ax=ax, alpha=0.8)
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, edge_color="#10B981", width=3.8, ax=ax, alpha=1.0)
            
            # Active Corridor Transit Nodes
            nx.draw_networkx_nodes(self.graph, pos, nodelist=transit_nodes, node_color="#10B981",
                                   node_size=1050, edgecolors="#34D399", linewidths=2.5, ax=ax)
            nx.draw_networkx_labels(self.graph, pos, labels={n: n for n in transit_nodes},
                                    font_size=9, font_family="sans-serif", font_color="#FFFFFF", font_weight="bold", ax=ax)

        # Edge distance labels
        edge_labels = {(u, v): f"{d['weight']} km" for u, v, d in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=7, font_color="#64748B",
                                     bbox=dict(facecolor="#0B0F19", edgecolor="none", alpha=0.8, pad=1), ax=ax)

        dest_name = highlighted_path[-1] if highlighted_path else "All Destinations"
        ax.set_title(f"HAULIX SATELLITE DISPATCH MAP — ACTIVE CORRIDOR TO [{dest_name.upper()}]",
                     fontsize=11, fontweight="800", pad=16, color="#F8FAFC", letterspacing=1.5)
        ax.axis("off")
        fig.tight_layout()
        return fig
