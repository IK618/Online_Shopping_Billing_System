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
        # Case-insensitive resolution of destination node
        target_node = None
        for node in self.graph.nodes():
            if node.lower() == destination.strip().lower():
                target_node = node
                break

        if not target_node:
            return ([CENTRAL_WAREHOUSE, destination], 0.0)

        # 1. NetworkX shortest path
        nx_path = nx.shortest_path(self.graph, source=CENTRAL_WAREHOUSE, target=target_node, weight="weight")
        nx_dist = nx.shortest_path_length(self.graph, source=CENTRAL_WAREHOUSE, target=target_node, weight="weight")

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

        scipy_dist = dist_matrix[node_to_idx[target_node]]
        return nx_path, float(scipy_dist)

    # High-precision geographic GPS coordinates (Latitude, Longitude) for India Logistics Hubs
    CITY_GPS = {
        "Bengaluru (Hub)": (12.9716, 77.5946),
        "Chennai": (13.0827, 80.2707),
        "Kochi": (9.9312, 76.2673),
        "Hyderabad": (17.3850, 78.4867),
        "Vijayawada": (16.5062, 80.6480),
        "Visakhapatnam": (17.6868, 83.2185),
        "Pune": (18.5204, 73.8567),
        "Mumbai": (19.0760, 72.8777),
        "Nagpur": (21.1458, 79.0882),
        "Bhopal": (23.2599, 77.4126),
        "Ahmedabad": (23.0225, 72.5714),
        "Bhubaneswar": (20.2961, 85.8245),
        "Kolkata": (22.5726, 88.3639),
        "Jaipur": (26.9124, 75.7873),
        "Delhi": (28.6139, 77.2090),
        "Lucknow": (26.8467, 80.9462),
        "Chandigarh": (30.7333, 76.7794),
    }

    # Approximate 2D canvas coordinates for static Matplotlib visualization
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

    def interpolate_delivery_gps(self, path: List[str], progress: float):
        """
        Calculates live GPS coordinates of the delivery person along the Dijkstra corridor.
        progress: float from 0.0 (Warehouse) to 1.0 (Customer Destination).
        Returns: (curr_lat, curr_lon, segment_name, speed_kmh, next_waypoint)
        """
        if not path or len(path) == 1:
            hub = path[0] if path else CENTRAL_WAREHOUSE
            lat, lon = self.CITY_GPS.get(hub, (12.9716, 77.5946))
            return lat, lon, f"At {hub}", 0, hub

        progress = max(0.0, min(1.0, float(progress)))
        total_segments = len(path) - 1
        segment_float = progress * total_segments
        seg_idx = min(int(segment_float), total_segments - 1)
        sub_progress = segment_float - seg_idx

        city_a = path[seg_idx]
        city_b = path[seg_idx + 1]

        lat_a, lon_a = self.CITY_GPS[city_a]
        lat_b, lon_b = self.CITY_GPS[city_b]

        curr_lat = lat_a + (lat_b - lat_a) * sub_progress
        curr_lon = lon_a + (lon_b - lon_a) * sub_progress

        segment_name = f"{city_a} ➔ {city_b}"
        speed = 0 if (progress >= 1.0 or progress <= 0.0) else 65
        next_waypoint = city_b if progress < 1.0 else "Delivered to Customer"

        return curr_lat, curr_lon, segment_name, speed, next_waypoint

    def create_interactive_deck(self, path: List[str], driver_lat: float, driver_lon: float, target_city: str):
        """
        Creates an interactive 3D WebGL OpenStreetMap / PyDeck live tracker.
        Renders the active corridor and moving delivery vehicle pin.
        """
        import pydeck as pdk
        import pandas as pd

        # 1. Path Coordinates for glowing highway corridor
        path_coords = [[self.CITY_GPS[city][1], self.CITY_GPS[city][0]] for city in path if city in self.CITY_GPS]
        path_df = pd.DataFrame([{"path": path_coords, "name": "Active Freight Corridor"}])

        # 2. Hub Waypoints
        hub_data = []
        for city in path:
            if city in self.CITY_GPS:
                lat, lon = self.CITY_GPS[city]
                is_hub = (city == CENTRAL_WAREHOUSE)
                is_dest = (city == target_city)
                color = [245, 158, 11, 230] if is_hub else ([56, 189, 248, 230] if is_dest else [148, 163, 184, 200])
                radius = 32000 if (is_hub or is_dest) else 18000
                hub_data.append({"city": city, "lat": lat, "lon": lon, "color": color, "radius": radius})
        hubs_df = pd.DataFrame(hub_data)

        # 3. Live Delivery Driver Marker
        driver_df = pd.DataFrame([{
            "lat": driver_lat,
            "lon": driver_lon,
            "label": "Delivery Vehicle (In Transit)",
            "color": [16, 185, 129, 255],
            "radius": 42000
        }])

        layers = [
            # Glowing Highway Path
            pdk.Layer(
                "PathLayer",
                data=path_df,
                get_path="path",
                get_color=[16, 185, 129, 220],
                width_min_pixels=4,
                width_max_pixels=8,
            ),
            # Regional Waypoint Nodes
            pdk.Layer(
                "ScatterplotLayer",
                data=hubs_df,
                get_position="[lon, lat]",
                get_color="color",
                get_radius="radius",
                pickable=True,
            ),
            # Moving Delivery Vehicle
            pdk.Layer(
                "ScatterplotLayer",
                data=driver_df,
                get_position="[lon, lat]",
                get_color="color",
                get_radius="radius",
                pickable=True,
            )
        ]

        view_state = pdk.ViewState(
            latitude=driver_lat,
            longitude=driver_lon,
            zoom=4.8,
            pitch=30,
            bearing=0
        )

        return pdk.Deck(
            layers=layers,
            initial_view_state=view_state,
            tooltip={"text": "{city}\n{label}"}
        )


    def generate_route_plot(self, highlighted_path: List[str] = None):
        """
        Renders a polished dark-slate Matplotlib visualization for SmartCart Logistics.
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

        # 4. Highlighted Optimal Route (Glowing Emerald Neon)
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
        ax.set_title(f"SMARTCART SATELLITE DISPATCH MAP — ACTIVE CORRIDOR TO [{dest_name.upper()}]",
                     fontsize=11, fontweight="800", pad=16, color="#F8FAFC")
        ax.axis("off")
        fig.tight_layout()
        return fig
