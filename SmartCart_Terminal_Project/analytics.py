"""
analytics.py
Business Intelligence & Sales Analytics Dashboard
Demonstrates:
  - Session 10: NumPy (ndarray, array creation, mean, sum, max, min, matrix reshaping)
  - Session 10: Matplotlib (Subplots, bar charts, line plots, markers, gridlines)
"""

import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
import logging
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

import numpy as np
import matplotlib.pyplot as plt
import database


def compute_sales_metrics():
    """
    Fetches raw order transactions and uses NumPy arrays for vectorized calculations.
    """
    orders = database.get_order_history(limit=100)
    if not orders:
        # Return fallback demo data if database is fresh
        totals = np.array([3499.0, 1899.0, 5499.0, 1299.0, 899.0, 2199.0, 1149.0])
    else:
        totals = np.array([float(row["total"]) for row in orders])

    metrics = {
        "total_revenue": float(np.sum(totals)),
        "average_order_value": float(np.mean(totals)),
        "max_order_value": float(np.max(totals)),
        "min_order_value": float(np.min(totals)),
        "order_count": int(totals.size),
        "revenue_std_dev": float(np.std(totals))
    }
    return metrics


def generate_sales_dashboard():
    """
    Generates a 2-panel Matplotlib dashboard:
      1. Bestselling Product Categories (Bar Chart)
      2. Daily Sales Trend (Line Plot with markers)
    """
    # 1. Product Categories & Sales Volume
    categories = ["Electronics", "Furniture", "Fashion", "Kitchen", "Groceries"]
    sales_units = np.array([45, 12, 38, 24, 65])
    revenue_thousands = np.array([125.4, 65.9, 34.2, 27.6, 22.7])

    # 2. Daily Sales trend over 7 days
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    daily_revenue = np.array([14.5, 18.2, 12.0, 22.4, 28.9, 35.2, 31.0])

    # Create Matplotlib Figure with 2 Subplots in Modern Dark Theme
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), facecolor="#0B0F19")
    ax1.set_facecolor("#131C2E")
    ax2.set_facecolor("#131C2E")

    # Spines styling
    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_color("#222F43")
        ax.tick_params(colors="#94A3B8", labelsize=8.5)

    # Panel 1: Bar Chart (SmartCart category distribution)
    bar_colors = ["#38BDF8", "#10B981", "#F59E0B", "#A855F7", "#EC4899"]
    bars = ax1.bar(categories, revenue_thousands, color=bar_colors, width=0.52, edgecolor="#222F43", linewidth=1.2)
    ax1.set_title("REVENUE BY PRODUCT CATEGORY (INR '000)", fontsize=10, fontweight="bold", pad=12, color="#F8FAFC")
    ax1.set_ylabel("Revenue (INR '000)", color="#94A3B8", fontsize=9)
    ax1.grid(axis="y", linestyle="--", alpha=0.2, color="#94A3B8")

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f"INR {height:.1f}k",
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 4), textcoords="offset points",
                     ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#F8FAFC")

    # Panel 2: Line Plot with Area Glow Fill (Velocity Telemetry Curve)
    ax2.fill_between(days, daily_revenue, color="#38BDF8", alpha=0.15)
    ax2.plot(days, daily_revenue, color="#38BDF8", marker="o", linewidth=2.8, markersize=7,
             markerfacecolor="#F8FAFC", markeredgecolor="#0284C7", markeredgewidth=2, label="Daily Inflow")
    ax2.set_title("WEEKLY REVENUE PERFORMANCE (INR '000)", fontsize=10, fontweight="bold", pad=12, color="#F8FAFC")
    ax2.set_ylabel("Daily Velocity (INR '000)", color="#94A3B8", fontsize=9)
    ax2.grid(True, linestyle="--", alpha=0.2, color="#94A3B8")
    ax2.legend(loc="upper left", facecolor="#131C2E", edgecolor="#222F43", labelcolor="#F8FAFC", fontsize=8.5)

    fig.suptitle("SMARTCART BUSINESS INTELLIGENCE & TELEMETRY ENGINE", fontsize=11, fontweight="bold", y=1.02, color="#F8FAFC")
    fig.tight_layout()
    return fig
