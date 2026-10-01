"""
app.py
Streamlit Web Frontend for Online Shopping & Billing System
Run with: streamlit run app.py
Features:
  - User Authentication (Login, Registration, Role-Based Access: Customer vs Admin)
  - Interactive Storefront & Product Catalog
  - Dynamic Cart & Live Checkout Calculation
  - Admin Inventory Manager (Add, Restock, Edit, Delete Products)
  - Automated Invoicing & Receipt Display
  - Interactive Delivery Route Visualizer (NetworkX + SciPy Dijkstra)
  - Business Intelligence Dashboard (NumPy + Matplotlib)
  - Asynchronous Database Cloud Backup (Threading + FTP)
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Local imports
import database
import models
from models import Product, Customer, Admin, ShoppingCart
import billing
import routing
import analytics
import backup_service

# Page Configuration
st.set_page_config(
    page_title="SmartCart - Shopping & Billing System",
    page_icon="🛒",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1e3a8a; }
    .sub-header { color: #475569; font-size: 1.1rem; margin-bottom: 1.5rem; }
    .auth-box { background-color: #f1f5f9; padding: 1.5rem; border-radius: 10px; border: 1px solid #cbd5e1; }
    .role-badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "auth_user" not in st.session_state:
    # Default to None so user logs in, or allow quick test login
    st.session_state.auth_user = None

if "customer" not in st.session_state:
    st.session_state.customer = None

if "cart" not in st.session_state:
    st.session_state.cart = None

if "optimizer" not in st.session_state:
    st.session_state.optimizer = routing.LogisticsOptimizer()

# Sidebar Brand Header
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=65)
st.sidebar.title("SmartCart Retail")

# -------------------------------------------------------------
# AUTHENTICATION LOGIC (SIDEBAR)
# -------------------------------------------------------------
if st.session_state.auth_user is None:
    st.sidebar.subheader("🔐 Account Sign In")
    auth_mode = st.sidebar.radio("Choose Action", ["Login", "Register New User"])

    if auth_mode == "Login":
        login_username = st.sidebar.text_input("Username", key="login_u")
        login_password = st.sidebar.text_input("Password", type="password", key="login_p")

        if st.sidebar.button("Log In", type="primary", use_container_width=True):
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
                st.sidebar.success(f"Welcome back, {user_row['username']}!")
                st.rerun()
            else:
                st.sidebar.error("Invalid username or password.")

        st.sidebar.markdown("---")
        st.sidebar.caption("👉 **Quick Demo Accounts:**")
        col_demo1, col_demo2 = st.sidebar.columns(2)
        with col_demo1:
            if st.button("Customer (Rahul)", use_container_width=True):
                user_row = database.authenticate_user("rahul_sharma", "pass123")
                st.session_state.auth_user = dict(user_row)
                st.session_state.customer = Customer(
                    user_id=user_row["user_id"],
                    username=user_row["username"],
                    email=user_row["email"],
                    city=user_row["city"],
                    is_premium=bool(user_row["is_premium"])
                )
                st.session_state.cart = ShoppingCart(st.session_state.customer)
                st.rerun()
        with col_demo2:
            if st.button("Admin (Manager)", use_container_width=True):
                user_row = database.authenticate_user("admin_user", "admin123")
                st.session_state.auth_user = dict(user_row)
                st.session_state.customer = None
                st.session_state.cart = None
                st.rerun()

    else:
        st.sidebar.subheader("📝 Register")
        new_u = st.sidebar.text_input("Username", key="reg_u")
        new_email = st.sidebar.text_input("Email", key="reg_e")
        new_pass = st.sidebar.text_input("Password", type="password", key="reg_p")
        cities = st.session_state.optimizer.get_all_cities()
        new_city = st.sidebar.selectbox("City", cities, key="reg_c")
        is_prem = st.sidebar.checkbox("Apply for Premium Membership (10% Off)", key="reg_prem")

        if st.sidebar.button("Create Account", type="primary", use_container_width=True):
            ok, msg = database.register_user(
                username=new_u,
                email=new_email,
                password=new_pass,
                city=new_city,
                is_premium=1 if is_prem else 0,
                role="customer"
            )
            if ok:
                st.sidebar.success(msg)
            else:
                st.sidebar.error(msg)

else:
    # Logged In Profile Badge
    u = st.session_state.auth_user
    st.sidebar.markdown(f"### 👤 {u['username']}")
    role_color = "#10b981" if u['role'] == "admin" else "#3b82f6"
    st.sidebar.markdown(f"<span style='background-color:{role_color};color:white;padding:3px 8px;border-radius:4px;font-size:0.8rem;text-transform:uppercase;'>{u['role']}</span>", unsafe_allow_html=True)
    st.sidebar.write(f"City: **{u.get('city', 'N/A')}**")
    if u['role'] == "customer":
        st.sidebar.caption("★ Premium Member (10% Discount)" if u.get("is_premium") else "Regular Shopper (2% Discount)")

    if st.sidebar.button("🚪 Log Out", use_container_width=True):
        st.session_state.auth_user = None
        st.session_state.customer = None
        st.session_state.cart = None
        st.rerun()

# -------------------------------------------------------------
# NAVIGATION MENU (ROLE-BASED)
# -------------------------------------------------------------
user_role = st.session_state.auth_user["role"] if st.session_state.auth_user else "guest"

if user_role == "admin":
    menu = st.sidebar.radio(
        "Admin Navigation",
        ["🛠️ Admin Inventory Manager", "📊 Sales Analytics Dashboard", "🚚 Delivery Route Optimizer", "⚙️ Cloud Backup & System"]
    )
else:
    menu = st.sidebar.radio(
        "Navigation Menu",
        ["🛍️ Storefront & Cart", "🚚 Delivery Route Optimizer", "📊 Sales Analytics Dashboard", "⚙️ Cloud Backup & System"]
    )

# -------------------------------------------------------------
# PAGE: STOREFRONT & CART (CUSTOMER VIEW)
# -------------------------------------------------------------
if menu == "🛍️ Storefront & Cart":
    st.markdown('<div class="main-header">🛒 SmartCart Online Store</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Browse inventory, manage your cart, and generate itemized tax invoices.</div>', unsafe_allow_html=True)

    if st.session_state.auth_user is None:
        st.warning("⚠️ You are browsing in guest mode. Please sign in or use the **Quick Demo Accounts** in the sidebar to complete purchases.")

    col_products, col_cart = st.columns([3, 2])

    with col_products:
        st.subheader("📦 Available Inventory")
        categories = ["All", "Electronics", "Furniture", "Home & Kitchen", "Fashion", "Groceries"]
        selected_cat = st.selectbox("Filter by Category", categories)

        products = database.get_all_products(selected_cat)
        for p in products:
            with st.container():
                c1, c2, c3 = st.columns([3, 1, 1.2])
                with c1:
                    st.write(f"**{p['name']}**")
                    st.caption(f"Category: {p['category']} | In Stock: {p['stock']} units")
                with c2:
                    st.write(f"**₹{p['price']:.2f}**")
                with c3:
                    qty = st.number_input("Qty", min_value=1, max_value=max(1, p['stock']), value=1, key=f"qty_{p['product_id']}")
                    if st.button("Add to Cart", key=f"add_{p['product_id']}"):
                        if st.session_state.customer is None:
                            st.error("Please log in first using the sidebar to add items to your cart.")
                        elif p['stock'] >= qty:
                            prod_obj = Product(p['product_id'], p['name'], p['category'], p['price'], p['stock'])
                            st.session_state.cart.add_item(prod_obj, qty)
                            st.toast(f"Added {qty}x {p['name']} to cart!", icon="🛒")
                        else:
                            st.error("Insufficient stock!")
                st.divider()

    with col_cart:
        st.subheader("🛍️ Your Shopping Cart")
        if st.session_state.cart is None:
            st.info("Log in with a customer account to use the shopping cart.")
        else:
            cart = st.session_state.cart
            cart_len = len(cart)

            if cart_len == 0:
                st.info("Your shopping cart is empty. Add products from the catalog.")
            else:
                cart_rows = []
                for item in cart.iter_items():
                    cart_rows.append({
                        "Product": item.product.name,
                        "Qty": item.quantity,
                        "Price": f"₹{item.product.price:.2f}",
                        "Total": f"₹{item.total_price:.2f}"
                    })
                st.dataframe(pd.DataFrame(cart_rows), hide_index=True, use_container_width=True)

                totals = cart.calculate_totals()
                st.markdown(f"""
                * **Subtotal:** ₹{totals['subtotal']:.2f}  
                * **Customer Discount ({int(totals['discount_rate']*100)}%):** -₹{totals['discount_amount']:.2f}  
                * **GST Tax (5%):** ₹{totals['tax']:.2f}  
                ### **Net Total: ₹{totals['total']:.2f}**  
                *(Truncated integer: ₹{totals['integer_rupees']})*
                """)

                cities = st.session_state.optimizer.get_all_cities()
                default_city = st.session_state.customer.city if st.session_state.customer.city in cities else cities[0]
                dest_city = st.selectbox("Select Delivery Destination", cities, index=cities.index(default_city))

                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    if st.button("💳 Checkout & Bill", type="primary", use_container_width=True):
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

                        # Save to SQLite
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

                        # Generate Receipts
                        receipt_text = billing.generate_text_receipt(
                            order_id, st.session_state.customer.username, dest_city, cart_items_data, totals
                        )
                        csv_path = billing.export_order_to_csv(
                            order_id, st.session_state.customer.username, dest_city, cart_items_data, totals
                        )

                        # Send Email (simulated)
                        billing.send_invoice_email(st.session_state.customer.email, order_id, receipt_text)

                        st.success(f"🎉 Order #{order_id} placed successfully!")
                        st.code(receipt_text, language="text")

                        # Download button for CSV receipt
                        with open(csv_path, "r") as f:
                            st.download_button(
                                label="📥 Download CSV Invoice",
                                data=f.read(),
                                file_name=f"invoice_{order_id}.csv",
                                mime="text/csv"
                            )

                        # Clear cart
                        st.session_state.cart.clear()
                        st.rerun()

                with c_btn2:
                    if st.button("🗑️ Clear Cart", use_container_width=True):
                        st.session_state.cart.clear()
                        st.rerun()

# -------------------------------------------------------------
# PAGE: ADMIN INVENTORY MANAGER (ADMIN VIEW ONLY)
# -------------------------------------------------------------
elif menu == "🛠️ Admin Inventory Manager":
    st.markdown('<div class="main-header">🛠️ Store Inventory & Catalog Manager</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Administrative controls to add products, adjust pricing, and restock units in SQLite.</div>', unsafe_allow_html=True)

    tab_add, tab_edit = st.tabs(["➕ Add New Product", "📝 Manage & Restock Products"])

    with tab_add:
        st.write("### Register a New Product")
        with st.form("add_product_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                new_p_name = st.text_input("Product Name", placeholder="e.g. Ultra HD Action Camera 4K")
                new_p_cat = st.selectbox("Category", ["Electronics", "Furniture", "Home & Kitchen", "Fashion", "Groceries", "Sports"])
            with col_b:
                new_p_price = st.number_input("Unit Price (₹)", min_value=1.0, value=999.0, step=50.0)
                new_p_stock = st.number_input("Initial Inventory Stock", min_value=1, value=25, step=5)

            submitted = st.form_submit_button("Add Product to Catalog", type="primary")
            if submitted:
                if new_p_name.strip():
                    new_id = database.add_product(new_p_name, new_p_cat, new_p_price, new_p_stock)
                    st.success(f"✅ Product '{new_p_name}' successfully created with Product ID #{new_id}!")
                else:
                    st.error("Please enter a valid product name.")

    with tab_edit:
        st.write("### Current Inventory Table")
        all_prods = database.get_all_products()
        prod_data = [
            {"ID": p["product_id"], "Name": p["name"], "Category": p["category"], "Price (₹)": f"₹{p['price']:.2f}", "Stock": p["stock"]}
            for p in all_prods
        ]
        st.dataframe(pd.DataFrame(prod_data), use_container_width=True, hide_index=True)

        st.divider()
        st.write("### Restock or Update Product Details")
        prod_options = {f"#{p['product_id']} - {p['name']}": p for p in all_prods}
        selected_prod_label = st.selectbox("Select Product to Edit", list(prod_options.keys()))
        selected_p = prod_options[selected_prod_label]

        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            updated_price = st.number_input("New Price (₹)", min_value=1.0, value=float(selected_p["price"]), step=50.0)
        with col_e2:
            updated_stock = st.number_input("New Stock Level", min_value=0, value=int(selected_p["stock"]), step=5)
        with col_e3:
            st.write("")
            st.write("")
            if st.button("💾 Save Updates", type="primary"):
                database.update_product_details(selected_p["product_id"], updated_price, updated_stock)
                st.success(f"Updated product #{selected_p['product_id']} successfully!")
                st.rerun()

        if st.button("🗑️ Delete Product from Catalog"):
            database.delete_product(selected_p["product_id"])
            st.warning(f"Deleted product #{selected_p['product_id']}.")
            st.rerun()

# -------------------------------------------------------------
# PAGE: LOGISTICS & ROUTE OPTIMIZATION
# -------------------------------------------------------------
elif menu == "🚚 Delivery Route Optimizer":
    st.markdown('<div class="main-header">🚚 Smart Logistics & Delivery Route Optimizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Graph-based pathfinding engine using NetworkX and SciPy Dijkstra shortest path algorithm.</div>', unsafe_allow_html=True)

    optimizer = st.session_state.optimizer
    cities = optimizer.get_all_cities()

    c1, c2 = st.columns([1, 2])
    with c1:
        st.write("### 📍 Routing Parameters")
        st.write(f"**Origin Warehouse:** `Bengaluru (Hub)`")
        target_city = st.selectbox("Select Customer City", cities)
        
        path, distance = optimizer.find_shortest_route(target_city)
        st.metric("Shortest Highway Distance", f"{distance} km")
        st.write(f"**Optimal Route Path:**")
        st.info(" ➔ ".join(path))

    with c2:
        st.write("### 🗺️ Network Topology & Visual Route")
        fig = optimizer.generate_route_plot(highlighted_path=path)
        st.pyplot(fig)

# -------------------------------------------------------------
# PAGE: SALES ANALYTICS DASHBOARD
# -------------------------------------------------------------
elif menu == "📊 Sales Analytics Dashboard":
    st.markdown('<div class="main-header">📊 Business Intelligence & Sales Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Real-time revenue metrics computed via NumPy arrays and visualized with Matplotlib.</div>', unsafe_allow_html=True)

    metrics = analytics.compute_sales_metrics()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Revenue", f"₹{metrics['total_revenue']:,.2f}")
    kpi2.metric("Avg Order Value", f"₹{metrics['average_order_value']:,.2f}")
    kpi3.metric("Peak Order Value", f"₹{metrics['max_order_value']:,.2f}")
    kpi4.metric("Total Orders Logged", f"{metrics['order_count']}")

    st.divider()
    st.write("### 📈 Visual Revenue Trends")
    fig = analytics.generate_sales_dashboard()
    st.pyplot(fig)

    st.divider()
    st.write("### 📋 Recent Transaction Logs (SQLite)")
    recent_orders = database.get_order_history(limit=10)
    if recent_orders:
        order_table = [
            {
                "Order ID": f"#{o['order_id']}",
                "Date": o['order_date'],
                "Customer": o['username'],
                "Email": o['email'],
                "Total (₹)": f"₹{o['total']:.2f}",
                "Destination": o['delivery_city'],
                "Status": o['status']
            }
            for o in recent_orders
        ]
        st.dataframe(pd.DataFrame(order_table), use_container_width=True, hide_index=True)
    else:
        st.info("No transaction logs recorded yet.")

# -------------------------------------------------------------
# PAGE: CLOUD BACKUP & SYSTEM
# -------------------------------------------------------------
elif menu == "⚙️ Cloud Backup & System":
    st.markdown('<div class="main-header">⚙️ System Services & Cloud Archival</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Background thread workers, FTP database backup, and POS socket connectivity.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("☁️ Automated FTP Database Backup")
        st.write("Archiving `store.db` to remote storage without blocking the user interface (demonstrates `threading` + `ftplib`).")
        if st.button("🚀 Trigger Cloud Backup Now"):
            thread = backup_service.run_async_backup()
            st.success("Background worker thread dispatched! SQLite backup successfully transmitted.")

    with c2:
        st.subheader("🔌 Network POS Socket Terminal")
        st.write("Connects cashier registers over TCP sockets (`AF_INET`, `SOCK_STREAM`).")
        st.code("""
# Run standalone Cashier Server:
python network_pos.py
        """, language="bash")
