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
import hashlib
from typing import List, Tuple, Dict, Any, Optional

DB_FILE = os.path.join(os.path.dirname(__file__), "store.db")


def hash_password(password: str) -> str:
    """Hashes password with SHA-256 and salt for secure storage."""
    salt = "smartcart_salt_2026"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()


def get_connection():
    """Returns a SQLite connection object."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enables column-name indexing
    return conn


def init_database():
    """Creates all required tables if they don't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table with password_hash
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            city TEXT NOT NULL,
            is_premium INTEGER DEFAULT 0,
            role TEXT DEFAULT 'customer',
            password_hash TEXT DEFAULT ''
        )
    """)

    # Migration: Ensure password_hash column exists in existing DB
    cursor.execute("PRAGMA table_info(users)")
    user_columns = [col["name"] for col in cursor.fetchall()]
    if "password_hash" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT DEFAULT ''")


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
            ("rahul_sharma", "rahul.sharma@example.com", "Mumbai", 1, "customer", hash_password("pass123")),
            ("priya_patel", "priya.patel@example.com", "Ahmedabad", 0, "customer", hash_password("pass123")),
            ("ananya_sen", "ananya.sen@example.com", "Kolkata", 1, "customer", hash_password("pass123")),
            ("admin_user", "admin@smartstore.com", "Bengaluru", 0, "admin", hash_password("admin123"))
        ]
        cursor.executemany(
            "INSERT INTO users (username, email, city, is_premium, role, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
            sample_users
        )
    else:
        # Populate password_hash if empty for existing rows
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = 'admin_user' AND (password_hash IS NULL OR password_hash = '')", (hash_password("admin123"),))
        cursor.execute("UPDATE users SET password_hash = ? WHERE role = 'customer' AND (password_hash IS NULL OR password_hash = '')", (hash_password("pass123"),))

    conn.commit()
    conn.close()


def register_user(username: str, email: str, password: str, city: str, is_premium: int = 0, role: str = "customer") -> Tuple[bool, str]:
    """
    Registers a new user with hashed password.
    Returns (success: bool, message: str).
    """
    if not username or not password or not email:
        return False, "Username, email, and password are required."
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        pwd_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, email, city, is_premium, role, password_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username.strip(), email.strip(), city.strip(), is_premium, role, pwd_hash))
        conn.commit()
        return True, "Registration successful! You can now log in."
    except sqlite3.IntegrityError:
        return False, f"Username '{username}' is already taken. Please choose another."
    except Exception as e:
        return False, f"Registration error: {e}"
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> Optional[sqlite3.Row]:
    """
    Validates user credentials against stored SHA-256 hash.
    Returns user Row if valid, None otherwise.
    """
    conn = get_connection()
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    cursor.execute("""
        SELECT * FROM users
        WHERE username = ? AND password_hash = ?
    """, (username.strip(), pwd_hash))
    user = cursor.fetchone()
    conn.close()
    return user


def add_product(name: str, category: str, price: float, stock: int) -> int:
    """Admin function: Adds a new product to inventory."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (name, category, price, stock)
        VALUES (?, ?, ?, ?)
    """, (name.strip(), category.strip(), float(price), int(stock)))
    prod_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return prod_id


def update_product_details(product_id: int, price: float, stock: int) -> bool:
    """Admin function: Updates price and stock of an existing product."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products SET price = ?, stock = ? WHERE product_id = ?
    """, (float(price), int(stock), int(product_id)))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


def delete_product(product_id: int) -> bool:
    """Admin function: Deletes a product from the catalog."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = ?", (int(product_id),))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0



def get_product_categories() -> List[str]:
    """Fetches unique product categories sorted alphabetically."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL ORDER BY category ASC")
    rows = cursor.fetchall()
    conn.close()
    return [r["category"] for r in rows if r["category"]]


def get_all_products(category_filter: Optional[str] = None, category: Optional[str] = None) -> List[sqlite3.Row]:
    """Fetches all products, optionally filtered by category."""
    cat = category or category_filter
    conn = get_connection()
    cursor = conn.cursor()
    if cat and cat not in ("All", "All Categories"):
        cursor.execute("SELECT * FROM products WHERE category = ? ORDER BY price ASC", (cat,))
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
