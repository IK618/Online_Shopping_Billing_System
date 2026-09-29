"""
analytics.py
Business Intelligence & Sales Analytics Dashboard
Demonstrates:
  - Session 10: NumPy (ndarray, array creation, mean, sum, max, min, matrix reshaping)
  - Session 10: Matplotlib (Subplots, bar charts, line plots, markers, gridlines)
"""

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

    # Create Matplotlib Figure with 2 Subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), facecolor="#f8f9fa")

    # Panel 1: Bar Chart (Session 10: bar chart, labels, colors)
    bars = ax1.bar(categories, revenue_thousands, color=["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899"], width=0.55)
    ax1.set_title("Revenue by Product Category (₹ '000)", fontsize=11, fontweight="bold", pad=10)
    ax1.set_ylabel("Revenue (Thousands ₹)")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f"₹{height:.1f}k",
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points",
                     ha="center", va="bottom", fontsize=8, fontweight="bold")

    # Panel 2: Line Plot (Session 10: line plot, markers, line styles)
    ax2.plot(days, daily_revenue, color="#2563eb", marker="o", linewidth=2.5, markersize=7, label="Revenue Trend")
    ax2.set_title("Weekly Sales Performance (₹ '000)", fontsize=11, fontweight="bold", pad=10)
    ax2.set_ylabel("Daily Revenue (Thousands ₹)")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper left")

    fig.suptitle("SmartCart Business Intelligence & Revenue Analytics", fontsize=13, fontweight="bold", y=1.02)
    fig.tight_layout()
    return fig
