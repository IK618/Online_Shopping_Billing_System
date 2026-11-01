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

    # 1. Shops Table (billEX Multi-Tenant Store Identity)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shops (
            shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_name TEXT NOT NULL,
            owner_user_id INTEGER,
            address TEXT NOT NULL,
            gstin TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            city TEXT DEFAULT 'Bengaluru',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_user_id) REFERENCES users(user_id)
        )
    """)

    # 2. Users Table with password_hash & shop_id
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            city TEXT NOT NULL,
            is_premium INTEGER DEFAULT 0,
            role TEXT DEFAULT 'customer',
            password_hash TEXT DEFAULT '',
            shop_id INTEGER DEFAULT 1,
            full_name TEXT DEFAULT ''
        )
    """)

    # Migration: Ensure columns exist in users
    cursor.execute("PRAGMA table_info(users)")
    user_columns = [col["name"] for col in cursor.fetchall()]
    if "password_hash" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT DEFAULT ''")
    if "shop_id" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN shop_id INTEGER DEFAULT 1")
    if "full_name" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT DEFAULT ''")

    # 3. Products Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            shop_id INTEGER DEFAULT 1
        )
    """)
    cursor.execute("PRAGMA table_info(products)")
    prod_columns = [col["name"] for col in cursor.fetchall()]
    if "shop_id" not in prod_columns:
        cursor.execute("ALTER TABLE products ADD COLUMN shop_id INTEGER DEFAULT 1")

    # 4. Orders Table with shop and cashier attribution
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
            shop_id INTEGER DEFAULT 1,
            billed_by_user_id INTEGER,
            customer_name TEXT DEFAULT '',
            customer_phone TEXT DEFAULT '',
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (shop_id) REFERENCES shops (shop_id)
        )
    """)
    cursor.execute("PRAGMA table_info(orders)")
    order_columns = [col["name"] for col in cursor.fetchall()]
    if "shop_id" not in order_columns:
        cursor.execute("ALTER TABLE orders ADD COLUMN shop_id INTEGER DEFAULT 1")
    if "billed_by_user_id" not in order_columns:
        cursor.execute("ALTER TABLE orders ADD COLUMN billed_by_user_id INTEGER")
    if "customer_name" not in order_columns:
        cursor.execute("ALTER TABLE orders ADD COLUMN customer_name TEXT DEFAULT ''")
    if "customer_phone" not in order_columns:
        cursor.execute("ALTER TABLE orders ADD COLUMN customer_phone TEXT DEFAULT ''")

    # 5. Order Items Table
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
            ("rahul_sharma", "rahul.sharma@example.com", "Mumbai", 1, "customer", hash_password("pass123"), 1, "Rahul Sharma"),
            ("priya_patel", "priya.patel@example.com", "Ahmedabad", 0, "customer", hash_password("pass123"), 1, "Priya Patel"),
            ("ananya_sen", "ananya.sen@example.com", "Kolkata", 1, "customer", hash_password("pass123"), 1, "Ananya Sen"),
            ("admin_user", "admin@smartstore.com", "Bengaluru", 0, "admin", hash_password("admin123"), 1, "Store Administrator")
        ]
        cursor.executemany(
            "INSERT INTO users (username, email, city, is_premium, role, password_hash, shop_id, full_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            sample_users
        )
    else:
        # Populate password_hash & shop_id if empty for existing rows
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = 'admin_user' AND (password_hash IS NULL OR password_hash = '')", (hash_password("admin123"),))
        cursor.execute("UPDATE users SET password_hash = ? WHERE role = 'customer' AND (password_hash IS NULL OR password_hash = '')", (hash_password("pass123"),))
        cursor.execute("UPDATE users SET shop_id = 1 WHERE shop_id IS NULL OR shop_id = 0")
        cursor.execute("UPDATE users SET full_name = 'Store Administrator' WHERE username = 'admin_user' AND (full_name IS NULL OR full_name = '')")

    # Check and seed default shop (Apex Electronics & Retail)
    cursor.execute("SELECT COUNT(*) AS count FROM shops")
    if cursor.fetchone()["count"] == 0:
        cursor.execute("""
            INSERT INTO shops (shop_id, shop_name, owner_user_id, address, gstin, phone, city)
            VALUES (1, 'Apex Electronics & Retail', 4, 'Shop #14, Brigade Road, Bengaluru - 560001', '29ABCDE1234F1Z5', '+91 9876543210', 'Bengaluru')
        """)

    # Seed sample Cashiers for Apex Electronics if they don't exist
    cursor.execute("SELECT user_id FROM users WHERE username = 'cashier_priya'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (username, email, city, is_premium, role, password_hash, shop_id, full_name)
            VALUES (?, ?, ?, 0, 'cashier', ?, 1, ?)
        """, ('cashier_priya', 'priya@apexelectronics.com', 'Bengaluru', hash_password('cashier123'), 'Priya Patel (Cashier)'))

    cursor.execute("SELECT user_id FROM users WHERE username = 'cashier_arun'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (username, email, city, is_premium, role, password_hash, shop_id, full_name)
            VALUES (?, ?, ?, 0, 'cashier', ?, 1, ?)
        """, ('cashier_arun', 'arun@apexelectronics.com', 'Bengaluru', hash_password('cashier123'), 'Arun Verma (Cashier)'))

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
    Returns user Row with joined shop identity if valid, None otherwise.
    """
    conn = get_connection()
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    cursor.execute("""
        SELECT u.*, 
               s.shop_name, 
               s.address AS shop_address, 
               s.gstin AS shop_gstin, 
               s.phone AS shop_phone, 
               s.city AS shop_city
        FROM users u
        LEFT JOIN shops s ON u.shop_id = s.shop_id
        WHERE u.username = ? AND u.password_hash = ?
    """, (username.strip(), pwd_hash))
    user = cursor.fetchone()
    conn.close()
    return user


def get_shop(shop_id: int = 1) -> Optional[sqlite3.Row]:
    """Retrieves store identity details by shop_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shops WHERE shop_id = ?", (shop_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_shop(shop_id: int, shop_name: str, address: str, gstin: str, phone: str, city: str) -> bool:
    """Updates shop identity, physical address, GSTIN, and contact details."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE shops 
        SET shop_name = ?, address = ?, gstin = ?, phone = ?, city = ?
        WHERE shop_id = ?
    """, (shop_name.strip(), address.strip(), gstin.strip().upper(), phone.strip(), city.strip(), shop_id))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def register_shop_and_owner(shop_name: str, address: str, gstin: str, phone: str, city: str,
                            username: str, email: str, password: str, full_name: str = "") -> Tuple[bool, str, Optional[int]]:
    """
    Onboards a new shop owner with their physical store identity and creates an Admin user.
    Returns (success, message, shop_id).
    """
    if not shop_name or not address or not username or not password:
        return False, "Shop name, address, owner username, and password are required.", None
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username.strip(),))
        if cursor.fetchone():
            conn.close()
            return False, f"Username '{username}' is already in use.", None

        pwd_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, email, city, is_premium, role, password_hash, full_name)
            VALUES (?, ?, ?, 0, 'admin', ?, ?)
        """, (username.strip(), email.strip(), city.strip(), pwd_hash, full_name.strip() or username.strip()))
        owner_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO shops (shop_name, owner_user_id, address, gstin, phone, city)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (shop_name.strip(), owner_id, address.strip(), gstin.strip().upper(), phone.strip(), city.strip()))
        shop_id = cursor.lastrowid

        cursor.execute("UPDATE users SET shop_id = ? WHERE user_id = ?", (shop_id, owner_id))

        conn.commit()
        conn.close()
        return True, "Shop and Owner account successfully registered!", shop_id
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error registering shop: {e}", None


def get_shop_employees(shop_id: int) -> List[sqlite3.Row]:
    """Retrieves all employee cashier staff for a specific store."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, username, full_name, email, role, city, shop_id
        FROM users
        WHERE shop_id = ? AND role IN ('cashier', 'employee')
        ORDER BY user_id ASC
    """, (shop_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_shop_employee(shop_id: int, full_name: str, username: str, password: str, email: str = "") -> Tuple[bool, str, Optional[int]]:
    """Allows a store owner to create an employee cashier account with billing access."""
    if not username or not password or not full_name:
        return False, "Employee full name, username, and password are required.", None
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username.strip(),))
        if cursor.fetchone():
            conn.close()
            return False, f"Username '{username}' is already in use.", None

        cursor.execute("SELECT city FROM shops WHERE shop_id = ?", (shop_id,))
        shop_row = cursor.fetchone()
        shop_city = shop_row["city"] if shop_row else "Bengaluru"

        pwd_hash = hash_password(password)
        emp_email = email.strip() or f"{username.strip()}@store{shop_id}.local"
        cursor.execute("""
            INSERT INTO users (username, email, city, is_premium, role, password_hash, shop_id, full_name)
            VALUES (?, ?, ?, 0, 'cashier', ?, ?, ?)
        """, (username.strip(), emp_email, shop_city, pwd_hash, shop_id, full_name.strip()))
        emp_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return True, f"Employee '{full_name}' created successfully with Cashier Billing access!", emp_id
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error creating employee: {e}", None


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
               tax: float, total: float, delivery_city: str, items: List[Dict[str, Any]],
               shop_id: int = 1, billed_by_user_id: Optional[int] = None,
               customer_name: str = "", customer_phone: str = "") -> int:
    """Inserts a completed order and its associated line items with relational transaction integrity."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO orders (user_id, order_date, subtotal, discount, tax, total, delivery_city, shop_id, billed_by_user_id, customer_name, customer_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, order_date, subtotal, discount, tax, total, delivery_city, shop_id, billed_by_user_id or user_id, customer_name, customer_phone))
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


def get_detailed_orders(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves full orders including line items from order_items table using relational joins."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.order_id, o.order_date, u.username, u.email, o.subtotal, o.discount, o.tax, o.total, o.delivery_city, o.status
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        ORDER BY o.order_id DESC
        LIMIT ?
    """, (limit,))
    orders_rows = cursor.fetchall()
    
    detailed = []
    for o in orders_rows:
        order_dict = dict(o)
        cursor.execute("""
            SELECT oi.item_id, oi.product_id, p.name, oi.quantity, oi.unit_price, oi.total_price
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            WHERE oi.order_id = ?
        """, (order_dict["order_id"],))
        order_dict["items"] = [dict(it) for it in cursor.fetchall()]
        detailed.append(order_dict)
    conn.close()
    return detailed


# Initialize database automatically on module import
init_database()
seed_sample_data()
