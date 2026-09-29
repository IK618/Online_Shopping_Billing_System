"""
database.py
SQLite Database Layer for Online Shopping & Billing System
Demonstrates:
  - Session 9: sqlite3 connection, cursor, execute, commit, fetchall, close
  - Relational Schema: users, products, orders, order_items
  - CRUD operations: INSERT, SELECT, UPDATE, DELETE
  - SQL clauses: WHERE, ORDER BY, GROUP BY, INNER JOIN, LIKE, BETWEEN
"""

import sqlite3
import os
from typing import List, Tuple, Dict, Any, Optional

DB_FILE = os.path.join(os.path.dirname(__file__), "store.db")


def get_connection():
    """Returns a SQLite connection object."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enables column-name indexing
    return conn


def init_database():
    """Creates all required tables if they don't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            city TEXT NOT NULL,
            is_premium INTEGER DEFAULT 0,
            role TEXT DEFAULT 'customer'
        )
    """)

    # 2. Products Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # 3. Orders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            order_date TEXT NOT NULL,
            subtotal REAL NOT NULL,
            discount REAL NOT NULL,
            tax REAL NOT NULL,
            total REAL NOT NULL,
            delivery_city TEXT NOT NULL,
            status TEXT DEFAULT 'Confirmed',
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)

    # 4. Order Items Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    """)

    conn.commit()
    conn.close()


def seed_sample_data():
    """Populates the database with realistic sample items if empty."""
    conn = get_connection()
    cursor = conn.cursor()

    # Check if products already exist
    cursor.execute("SELECT COUNT(*) AS count FROM products")
    if cursor.fetchone()["count"] == 0:
        sample_products = [
            ("Wireless Noise-Canceling Headphones", "Electronics", 3499.00, 25),
            ("Mechanical RGB Gaming Keyboard", "Electronics", 2199.00, 18),
            ("Smart Fitness Band & Tracker", "Electronics", 1899.00, 30),
            ("Ergonomic Mesh Office Chair", "Furniture", 5499.00, 10),
            ("Stainless Steel Thermal Bottle (1L)", "Home & Kitchen", 599.00, 50),
            ("Cotton Casual Slim-Fit Shirt", "Fashion", 899.00, 40),
            ("Classic Leather Wallet & Card Holder", "Fashion", 499.00, 35),
            ("Organic Green Tea (Pack of 100 bags)", "Groceries", 349.00, 60),
            ("USB-C Fast Charging Hub (6-in-1)", "Electronics", 1299.00, 22),
            ("Ceramic Non-Stick Frying Pan", "Home & Kitchen", 1149.00, 15)
        ]
        cursor.executemany(
            "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
            sample_products
        )

    # Check if default users exist
    cursor.execute("SELECT COUNT(*) AS count FROM users")
    if cursor.fetchone()["count"] == 0:
        sample_users = [
            ("rahul_sharma", "rahul.sharma@example.com", "Mumbai", 1, "customer"),
            ("priya_patel", "priya.patel@example.com", "Ahmedabad", 0, "customer"),
            ("ananya_sen", "ananya.sen@example.com", "Kolkata", 1, "customer"),
            ("admin_user", "admin@smartstore.com", "Bengaluru", 0, "admin")
        ]
        cursor.executemany(
            "INSERT INTO users (username, email, city, is_premium, role) VALUES (?, ?, ?, ?, ?)",
            sample_users
        )

    conn.commit()
    conn.close()


def get_all_products(category_filter: Optional[str] = None) -> List[sqlite3.Row]:
    """Fetches all products, optionally filtered by category."""
    conn = get_connection()
    cursor = conn.cursor()
    if category_filter and category_filter != "All":
        cursor.execute("SELECT * FROM products WHERE category = ? ORDER BY price ASC", (category_filter,))
    else:
        cursor.execute("SELECT * FROM products ORDER BY category, name")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_product(product_id: int) -> Optional[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_product_stock(product_id: int, quantity_sold: int) -> bool:
    """Decrements inventory stock upon purchase."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT stock FROM products WHERE product_id = ?", (product_id,))
    row = cursor.fetchone()
    if row and row["stock"] >= quantity_sold:
        cursor.execute(
            "UPDATE products SET stock = stock - ? WHERE product_id = ?",
            (quantity_sold, product_id)
        )
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False


def save_order(user_id: int, order_date: str, subtotal: float, discount: float,
               tax: float, total: float, delivery_city: str, items: List[Dict[str, Any]]) -> int:
    """Inserts a completed order and its associated line items with relational transaction integrity."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO orders (user_id, order_date, subtotal, discount, tax, total, delivery_city)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, order_date, subtotal, discount, tax, total, delivery_city))
        order_id = cursor.lastrowid

        for item in items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, item["product_id"], item["quantity"], item["unit_price"], item["total_price"]))
            
            # Decrement inventory stock
            cursor.execute(
                "UPDATE products SET stock = stock - ? WHERE product_id = ?",
                (item["quantity"], item["product_id"])
            )

        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_order_history(limit: int = 50) -> List[sqlite3.Row]:
    """Retrieves past orders with user details using SQL INNER JOIN."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.order_id, o.order_date, u.username, u.email, o.total, o.delivery_city, o.status
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        ORDER BY o.order_id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows


# Initialize database automatically on module import
init_database()
seed_sample_data()
