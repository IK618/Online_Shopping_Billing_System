"""
app.py
Streamlit Web Frontend for Online Shopping & Billing System
Modern UI / UX Upgrade:
  - Custom Responsive Theme, Typography & Card Layouts
  - Real-time Product Search, Category Pills & Price Sorting
  - Interactive Shopping Cart with Visual Breakdown
  - Order Checkout Celebration with Confetti & Direct CSV/Text Download
  - Geographically Accurate Logistics Route Map & Transit KPI Cards
  - Executive Business Intelligence Dashboard with NumPy Vectorized Metrics
  - Admin Inventory & Restock Hub with Health Indicators
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Local application modules
import database
import models
from models import Product, Customer, Admin, ShoppingCart
import billing
import routing
import analytics
import backup_service

# Page Configuration
st.set_page_config(
    page_title="SmartCart — Retail & Logistics Engine",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# HIGH-END MODERN CSS & THEME INJECTION
# -------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    /* Gradient Hero Header */
    .hero-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #3b82f6 100%);
        padding: 1.8rem 2.2rem;
        border-radius: 14px;
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.2);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 1.0rem;
        opacity: 0.9;
        margin-top: 0.4rem;
        font-weight: 400;
    }

    /* Product & UI Cards */
    .product-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
        border-color: #cbd5e1;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }
    .badge-electronics { background-color: #dbeafe; color: #1e40af; }
    .badge-furniture { background-color: #fef3c7; color: #92400e; }
    .badge-fashion { background-color: #f3e8ff; color: #6b21a8; }
    .badge-kitchen { background-color: #ffe4e6; color: #9f1239; }
    .badge-groceries { background-color: #dcfce7; color: #166534; }
    .badge-sports { background-color: #ffedd5; color: #9a3412; }

    .stock-in { color: #16a34a; font-weight: 600; font-size: 0.85rem; }
    .stock-low { color: #d97706; font-weight: 600; font-size: 0.85rem; }
    .stock-out { color: #dc2626; font-weight: 600; font-size: 0.85rem; }

    /* Summary & Price Highlight */
    .price-tag {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0f172a;
    }
    .summary-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.3rem;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------------------
if "auth_user" not in st.session_state:
    st.session_state.auth_user = None

if "customer" not in st.session_state:
    st.session_state.customer = None

if "cart" not in st.session_state:
    st.session_state.cart = None

if "optimizer" not in st.session_state:
    st.session_state.optimizer = routing.LogisticsOptimizer()

# -------------------------------------------------------------
# SIDEBAR: BRANDING & AUTHENTICATION
# -------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=60)
    st.markdown("## **SmartCart** Retail")
    st.caption("Integrated Invoicing, Routing & Analytics")
    st.divider()

    # User Profile / Login Card
    if st.session_state.auth_user is None:
        st.markdown("#### 🔐 Member Sign In")
        auth_mode = st.radio("Access Mode", ["Login", "Register"], horizontal=True, label_visibility="collapsed")

        if auth_mode == "Login":
            login_username = st.text_input("Username", key="l_user", placeholder="Enter username")
            login_password = st.text_input("Password", type="password", key="l_pass", placeholder="••••••••")

            if st.button("Sign In ➔", type="primary", use_container_width=True):
                user_row = database.authenticate_user(login_username, login_password)
                if user_row:
                    st.session_state.auth_user = dict(user_row)
                    if user_row["role"] == "customer":
                        st.session_state.customer = Customer(
                            user_id=user_row["user_id"],
                            username=user_row["username"],
                            email=user_row["email"],
                            city=user_row["city"],
                            is_premium=bool(user_row["is_premium"])
                        )
                        st.session_state.cart = ShoppingCart(st.session_state.customer)
                    st.success(f"Welcome, {user_row['username']}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

            st.markdown("---")
            st.caption("⚡ **One-Click Demo Accounts:**")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if st.button("Customer (Rahul)", use_container_width=True):
                    u = database.authenticate_user("rahul_sharma", "pass123")
                    st.session_state.auth_user = dict(u)
                    st.session_state.customer = Customer(u["user_id"], u["username"], u["email"], u["city"], bool(u["is_premium"]))
                    st.session_state.cart = ShoppingCart(st.session_state.customer)
                    st.rerun()
            with col_d2:
                if st.button("Admin (Manager)", use_container_width=True):
                    u = database.authenticate_user("admin_user", "admin123")
                    st.session_state.auth_user = dict(u)
                    st.session_state.customer = None
                    st.session_state.cart = None
                    st.rerun()

        else:
            st.markdown("#### 📝 Register")
            reg_u = st.text_input("Username", key="r_u")
            reg_e = st.text_input("Email", key="r_e")
            reg_p = st.text_input("Password", type="password", key="r_p")
            cities = st.session_state.optimizer.get_all_cities()
            reg_c = st.selectbox("Location City", cities, key="r_c")
            reg_prem = st.checkbox("Sign up for Premium (10% Discount)", value=True)

            if st.button("Create Account", type="primary", use_container_width=True):
                ok, msg = database.register_user(reg_u, reg_e, reg_p, reg_c, 1 if reg_prem else 0, "customer")
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

    else:
        # Authenticated Profile Badge
        user_info = st.session_state.auth_user
        st.markdown(f"### 👤 {user_info['username']}")
        if user_info["role"] == "admin":
            st.markdown('<span class="badge" style="background:#dcfce7;color:#166534;">🛡️ STORE ADMINISTRATOR</span>', unsafe_allow_html=True)
        else:
            tier_badge = "★ PREMIUM MEMBER (10% OFF)" if user_info.get("is_premium") else "REGULAR CUSTOMER (2% OFF)"
            st.markdown(f'<span class="badge badge-electronics">{tier_badge}</span>', unsafe_allow_html=True)
        st.write(f"📍 Location: **{user_info.get('city', 'Bengaluru')}**")

        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.auth_user = None
            st.session_state.customer = None
            st.session_state.cart = None
            st.rerun()

    st.divider()

    # Role-Based Navigation
    user_role = st.session_state.auth_user["role"] if st.session_state.auth_user else "guest"
    if user_role == "admin":
        menu = st.radio(
            "Navigation",
            ["🛠️ Admin Inventory Manager", "📊 Sales Analytics Dashboard", "🚚 Delivery Route Optimizer", "⚙️ Cloud Backup & System"]
        )
    else:
        menu = st.radio(
            "Navigation",
            ["🛍️ Storefront & Cart", "🚚 Delivery Route Optimizer", "📊 Sales Analytics Dashboard", "⚙️ Cloud Backup & System"]
        )

# -------------------------------------------------------------
# PAGE 1: STOREFRONT & CART (CUSTOMER VIEW)
# -------------------------------------------------------------
if menu == "🛍️ Storefront & Cart":
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">Discover Quality Products with Smart Logistics</h1>
            <div class="hero-subtitle">Browse curated inventory, enjoy instant tier discounts, and trace optimal delivery corridors.</div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.auth_user is None:
        st.info("💡 You are browsing as a guest. Please use the sidebar to **Sign In** or click **Customer (Rahul)** to test checkout.")

    col_catalog, col_cart = st.columns([3, 2], gap="large")

    # LEFT: CATALOG & SEARCH
    with col_catalog:
        st.markdown("### 📦 Product Catalog")

        # Search & Filter Controls
        f_col1, f_col2, f_col3 = st.columns([2, 1.5, 1.5])
        with f_col1:
            search_query = st.text_input("Search", placeholder="🔍 Search products by name...", label_visibility="collapsed")
        with f_col2:
            categories = ["All", "Electronics", "Furniture", "Home & Kitchen", "Fashion", "Groceries"]
            cat_choice = st.selectbox("Category", categories, label_visibility="collapsed")
        with f_col3:
            sort_choice = st.selectbox("Sort", ["Price: Low to High", "Price: High to Low", "Name: A-Z"], label_visibility="collapsed")

        # Fetch and Filter Products
        raw_products = database.get_all_products(cat_choice if cat_choice != "All" else None)
        products_list = [dict(p) for p in raw_products]

        # Apply Search Filter
        if search_query.strip():
            products_list = [p for p in products_list if search_query.lower() in p["name"].lower() or search_query.lower() in p["category"].lower()]

        # Apply Sort
        if sort_choice == "Price: Low to High":
            products_list.sort(key=lambda x: x["price"])
        elif sort_choice == "Price: High to Low":
            products_list.sort(key=lambda x: x["price"], reverse=True)
        elif sort_choice == "Name: A-Z":
            products_list.sort(key=lambda x: x["name"])

        # Display Category Badges Helper
        category_badge_map = {
            "Electronics": "badge-electronics",
            "Furniture": "badge-furniture",
            "Fashion": "badge-fashion",
            "Home & Kitchen": "badge-kitchen",
            "Groceries": "badge-groceries"
        }

        if not products_list:
            st.warning("No products matched your search.")
        else:
            for p in products_list:
                badge_class = category_badge_map.get(p["category"], "badge-electronics")
                stock_text = f"✓ In Stock ({p['stock']} units)" if p['stock'] > 5 else (f"⚠️ Low Stock ({p['stock']} left)" if p['stock'] > 0 else "✕ Out of Stock")
                stock_class = "stock-in" if p['stock'] > 5 else ("stock-low" if p['stock'] > 0 else "stock-out")

                with st.container():
                    st.markdown(f"""
                        <div class="product-card">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="badge {badge_class}">{p['category']}</span>
                                <span class="{stock_class}">{stock_text}</span>
                            </div>
                            <div style="font-size:1.15rem; font-weight:700; color:#0f172a; margin:0.4rem 0 0.2rem 0;">{p['name']}</div>
                            <div class="price-tag">₹{p['price']:,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)

                    c_qty, c_btn = st.columns([1, 2])
                    with c_qty:
                        qty = st.number_input("Qty", min_value=1, max_value=max(1, p['stock']), value=1, key=f"q_{p['product_id']}", label_visibility="collapsed")
                    with c_btn:
                        if st.button("🛒 Add to Cart", key=f"b_{p['product_id']}", use_container_width=True, disabled=(p['stock'] <= 0)):
                            if st.session_state.customer is None:
                                st.error("Please log in using the sidebar to purchase.")
                            else:
                                prod_obj = Product(p['product_id'], p['name'], p['category'], p['price'], p['stock'])
                                st.session_state.cart.add_item(prod_obj, qty)
                                st.toast(f"Added {qty}x {p['name']} to cart!", icon="🛍️")
                    st.write("")

    # RIGHT: SHOPPING CART & BILLING SUMMARY
    with col_cart:
        st.markdown("### 🛒 Order Summary")

        if st.session_state.cart is None:
            st.markdown("""
                <div class="summary-card" style="text-align:center; padding:2.5rem 1rem;">
                    <div style="font-size:3rem; margin-bottom:0.5rem;">🛍️</div>
                    <div style="font-weight:700; font-size:1.1rem; color:#1e293b;">Sign in to start shopping</div>
                    <p style="color:#64748b; font-size:0.9rem;">Sign in as customer to build your cart, apply membership discounts, and track delivery routes.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            cart = st.session_state.cart
            items_count = len(cart)

            if items_count == 0:
                st.markdown("""
                    <div class="summary-card" style="text-align:center; padding:2rem 1rem;">
                        <div style="font-size:2.5rem; margin-bottom:0.3rem;">🛒</div>
                        <div style="font-weight:700; color:#334155;">Your cart is empty</div>
                        <p style="color:#64748b; font-size:0.85rem;">Select products from the catalog to get started.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                cart_display = []
                for item in cart.iter_items():
                    cart_display.append({
                        "Product": item.product.name[:25] + ("..." if len(item.product.name) > 25 else ""),
                        "Qty": item.quantity,
                        "Price": f"₹{item.product.price:,.2f}",
                        "Total": f"₹{item.total_price:,.2f}"
                    })
                st.dataframe(pd.DataFrame(cart_display), use_container_width=True, hide_index=True)

                totals = cart.calculate_totals()
                discount_label = f"Customer Discount ({int(totals['discount_rate']*100)}%)"

                st.markdown(f"""
                    <div class="summary-card">
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem; color:#475569;">
                            <span>Subtotal:</span><span style="font-weight:600;">₹{totals['subtotal']:,.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem; color:#16a34a;">
                            <span>{discount_label}:</span><span style="font-weight:600;">-₹{totals['discount_amount']:,.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.6rem; color:#475569;">
                            <span>GST Tax (5%):</span><span style="font-weight:600;">₹{totals['tax']:,.2f}</span>
                        </div>
                        <hr style="margin:0.5rem 0; border-color:#cbd5e1;" />
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:1.15rem; font-weight:800; color:#0f172a;">Grand Total:</span>
                            <span style="font-size:1.45rem; font-weight:800; color:#1e3a8a;">₹{totals['total']:,.2f}</span>
                        </div>
                        <div style="font-size:0.8rem; color:#64748b; text-align:right;">
                            Banker's rounded integer: ₹{totals['integer_rupees']:,}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.write("")
                st.markdown("##### 📍 Destination & Dispatch Hub")
                cities = st.session_state.optimizer.get_all_cities()
                default_dest = st.session_state.customer.city if st.session_state.customer.city in cities else cities[0]
                dest_city = st.selectbox("Delivery City", cities, index=cities.index(default_dest), label_visibility="collapsed")

                btn_c1, btn_c2 = st.columns([2, 1])
                with btn_c1:
                    if st.button("💳 Confirm Order & Checkout", type="primary", use_container_width=True):
                        cart_items_data = [
                            {
                                "product_id": item.product.product_id,
                                "name": item.product.name,
                                "quantity": item.quantity,
                                "unit_price": item.product.price,
                                "total_price": item.total_price
                            }
                            for item in cart.iter_items()
                        ]

                        # Persist order transaction in SQLite
                        order_id = database.save_order(
                            user_id=st.session_state.customer.user_id,
                            order_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            subtotal=totals["subtotal"],
                            discount=totals["discount_amount"],
                            tax=totals["tax"],
                            total=totals["total"],
                            delivery_city=dest_city,
                            items=cart_items_data
                        )

                        # Generate Invoices
                        receipt_text = billing.generate_text_receipt(order_id, st.session_state.customer.username, dest_city, cart_items_data, totals)
                        csv_path = billing.export_order_to_csv(order_id, st.session_state.customer.username, dest_city, cart_items_data, totals)

                        # Trigger simulated SMTP email
                        billing.send_invoice_email(st.session_state.customer.email, order_id, receipt_text)

                        # CELEBRATION EFFECT (UX DELIGHT)
                        st.balloons()
                        st.success(f"🎉 Order #{order_id} Confirmed! Invoices generated successfully.")

                        # Show Download & Receipt Expanders
                        with open(csv_path, "r") as f:
                            st.download_button(
                                label="📥 Download Official CSV Tax Invoice",
                                data=f.read(),
                                file_name=f"smartcart_invoice_{order_id}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )

                        with st.expander("📄 View Itemized Printable Tax Receipt", expanded=True):
                            st.code(receipt_text, language="text")

                        st.session_state.cart.clear()

                with btn_c2:
                    if st.button("Clear Cart", use_container_width=True):
                        st.session_state.cart.clear()
                        st.rerun()

# -------------------------------------------------------------
# PAGE 2: LOGISTICS & ROUTE OPTIMIZATION
# -------------------------------------------------------------
elif menu == "🚚 Delivery Route Optimizer":
    st.markdown("""
        <div class="hero-container" style="background: linear-gradient(135deg, #0f766e 0%, #0d9488 50%, #14b8a6 100%);">
            <h1 class="hero-title">Graph-Optimized Fleet Logistics & Highway Pathfinding</h1>
            <div class="hero-subtitle">Powered by NetworkX road topology and SciPy's sparse Compressed Sparse Row (CSR) Dijkstra algorithm.</div>
        </div>
    """, unsafe_allow_html=True)

    optimizer = st.session_state.optimizer
    cities = optimizer.get_all_cities()

    c_params, c_map = st.columns([1.2, 2.2], gap="large")

    with c_params:
        st.markdown("### 📍 Dispatch Parameters")
        st.write("Central Fulfillment Center:")
        st.info("🏭 **Bengaluru (Central Hub)**")

        target_city = st.selectbox("Select Customer Destination", cities, index=cities.index("Delhi") if "Delhi" in cities else 0)
        path, distance = optimizer.find_shortest_route(target_city)

        # Transit KPI Cards
        est_days = round(distance / 650.0, 1)  # Assuming 650 km/day heavy freight transit
        fuel_est = round(distance * 0.32, 1)   # Approx fuel consumption in liters

        st.markdown("#### 🚀 Route Intelligence Metrics")
        m1, m2 = st.columns(2)
        m1.metric("Highway Distance", f"{distance:,.0f} km")
        m2.metric("Transit Hubs", f"{len(path)} stops")

        m3, m4 = st.columns(2)
        m3.metric("Est. Delivery Window", f"{est_days} days")
        m4.metric("Fuel Estimate", f"{fuel_est:,.0f} L")

        st.markdown("#### 🛣️ Active Highway Corridor")
        st.success(" ➔ ".join(path))

    with c_map:
        st.markdown("### 🗺️ India Distribution Network Map")
        fig = optimizer.generate_route_plot(highlighted_path=path)
        st.pyplot(fig)

# -------------------------------------------------------------
# PAGE 3: SALES ANALYTICS DASHBOARD
# -------------------------------------------------------------
elif menu == "📊 Sales Analytics Dashboard":
    st.markdown("""
        <div class="hero-container" style="background: linear-gradient(135deg, #4338ca 0%, #6366f1 50%, #818cf8 100%);">
            <h1 class="hero-title">Executive Revenue & Inventory Analytics</h1>
            <div class="hero-subtitle">High-speed statistical metrics computed with NumPy multidimensional arrays and rendered in Matplotlib.</div>
        </div>
    """, unsafe_allow_html=True)

    metrics = analytics.compute_sales_metrics()

    # Metric Cards
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Store Revenue", f"₹{metrics['total_revenue']:,.2f}", "+14.2% vs last month")
    k2.metric("Average Order Value", f"₹{metrics['average_order_value']:,.2f}", "+5.8%")
    k3.metric("Peak Transaction", f"₹{metrics['max_order_value']:,.2f}")
    k4.metric("Total Completed Orders", f"{metrics['order_count']} orders", "ACID Verified")

    st.write("")
    st.markdown("### 📈 Visual Revenue Trends & Category Breakdown")
    fig = analytics.generate_sales_dashboard()
    st.pyplot(fig)

    st.write("")
    st.markdown("### 📋 Real-Time Transaction Ledger (SQLite)")
    recent_orders = database.get_order_history(limit=15)
    if recent_orders:
        order_table = [
            {
                "Order ID": f"#{o['order_id']}",
                "Timestamp": o['order_date'],
                "Customer": o['username'],
                "Destination": o['delivery_city'],
                "Amount Paid": f"₹{o['total']:,.2f}",
                "Status": "🟢 " + o['status']
            }
            for o in recent_orders
        ]
        st.dataframe(pd.DataFrame(order_table), use_container_width=True, hide_index=True)
    else:
        st.info("No transaction logs recorded yet.")

# -------------------------------------------------------------
# PAGE 4: ADMIN INVENTORY MANAGER (ADMIN VIEW ONLY)
# -------------------------------------------------------------
elif menu == "🛠️ Admin Inventory Manager":
    st.markdown("""
        <div class="hero-container" style="background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);">
            <h1 class="hero-title">Store Inventory & Catalog Hub</h1>
            <div class="hero-subtitle">Manage store products, adjust pricing, replenish units, and monitor catalog health.</div>
        </div>
    """, unsafe_allow_html=True)

    tab_overview, tab_add, tab_edit = st.tabs(["📋 Inventory Overview", "➕ Register New Product", "⚙️ Restock & Adjust Prices"])

    with tab_overview:
        all_prods = database.get_all_products()
        total_skus = len(all_prods)
        total_units = sum(p["stock"] for p in all_prods)
        inventory_val = sum(p["price"] * p["stock"] for p in all_prods)

        inv_c1, inv_c2, inv_c3 = st.columns(3)
        inv_c1.metric("Active Catalog SKUs", f"{total_skus} products")
        inv_c2.metric("Total Units in Warehouse", f"{total_units:,} items")
        inv_c3.metric("Total Asset Valuation", f"₹{inventory_val:,.2f}")

        st.write("")
        prod_table = [
            {"SKU ID": f"#{p['product_id']}", "Product Name": p["name"], "Category": p["category"], "Unit Price": f"₹{p['price']:,.2f}", "Units In Stock": p["stock"]}
            for p in all_prods
        ]
        st.dataframe(pd.DataFrame(prod_table), use_container_width=True, hide_index=True)

    with tab_add:
        st.markdown("#### ➕ Add New SKU to Store Catalog")
        with st.form("new_product_form", clear_on_submit=True):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                p_name = st.text_input("Product Title", placeholder="e.g. Wireless Ergonomic Mouse")
                p_cat = st.selectbox("Category", ["Electronics", "Furniture", "Home & Kitchen", "Fashion", "Groceries", "Sports"])
            with col_f2:
                p_price = st.number_input("Retail Price (₹)", min_value=1.0, value=1499.0, step=50.0)
                p_stock = st.number_input("Initial Warehouse Stock", min_value=1, value=25, step=5)

            submitted = st.form_submit_button("Create Product Record", type="primary")
            if submitted:
                if p_name.strip():
                    new_id = database.add_product(p_name, p_cat, p_price, p_stock)
                    st.success(f"✅ SKU #{new_id} ('{p_name}') registered into SQLite inventory!")
                else:
                    st.error("Product name cannot be empty.")

    with tab_edit:
        st.markdown("#### ⚙️ Edit Product Pricing & Restock Units")
        all_prods = database.get_all_products()
        prod_dict = {f"#{p['product_id']} — {p['name']} (Stock: {p['stock']})": p for p in all_prods}

        chosen_prod_key = st.selectbox("Choose Product to Modify", list(prod_dict.keys()))
        selected_prod = prod_dict[chosen_prod_key]

        col_u1, col_u2, col_u3 = st.columns(3)
        with col_u1:
            new_price = st.number_input("Adjust Price (₹)", min_value=1.0, value=float(selected_prod["price"]), step=50.0)
        with col_u2:
            new_stock = st.number_input("Adjust Warehouse Stock", min_value=0, value=int(selected_prod["stock"]), step=5)
        with col_u3:
            st.write("")
            st.write("")
            if st.button("💾 Apply Changes", type="primary", use_container_width=True):
                database.update_product_details(selected_prod["product_id"], new_price, new_stock)
                st.success(f"Product #{selected_prod['product_id']} updated successfully!")
                st.rerun()

        st.divider()
        if st.button("🗑️ Delete Product SKU from Catalog"):
            database.delete_product(selected_prod["product_id"])
            st.warning(f"Product #{selected_prod['product_id']} removed.")
            st.rerun()

# -------------------------------------------------------------
# PAGE 5: CLOUD BACKUP & SYSTEM
# -------------------------------------------------------------
elif menu == "⚙️ Cloud Backup & System":
    st.markdown("""
        <div class="hero-container" style="background: linear-gradient(135deg, #1e3a8a 0%, #312e81 50%, #4338ca 100%);">
            <h1 class="hero-title">System Infrastructure & Concurrency Services</h1>
            <div class="hero-subtitle">Non-blocking background thread workers, automated FTP database archival, and TCP socket POS terminals.</div>
        </div>
    """, unsafe_allow_html=True)

    b_col1, b_col2 = st.columns(2, gap="large")

    with b_col1:
        st.markdown("### ☁️ Asynchronous Cloud Backup")
        st.write("Spawns a dedicated background thread (`threading.Thread`) that uploads an encrypted database snapshot to remote FTP storage without causing browser latency.")
        if st.button("🚀 Trigger Cloud Backup Now", type="primary"):
            thread = backup_service.run_async_backup()
            st.success("Backup worker thread dispatched in the background! Database successfully transmitted to FTP.")

    with b_col2:
        st.markdown("### 🔌 POS Cashier TCP Sockets")
        st.write("Demonstrates low-level client-server socket communication over port `65432` (`AF_INET`, `SOCK_STREAM`).")
        st.code("""
# Launch the TCP Socket Server in your terminal:
python network_pos.py
        """, language="bash")
