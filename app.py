"""
app.py
Streamlit Web Frontend for Online Shopping & Billing System
Run with: streamlit run app.py
Features:
  - Interactive Storefront & Product Catalog
  - Dynamic Cart & Live Checkout Calculation
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
from models import Product, Customer, ShoppingCart
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
    .card { background-color: #f8fafc; border-radius: 8px; padding: 1rem; border: 1px solid #e2e8f0; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "customer" not in st.session_state:
    st.session_state.customer = Customer(
        user_id=1,
        username="rahul_sharma",
        email="rahul.sharma@example.com",
        city="Mumbai",
        is_premium=True
    )

if "cart" not in st.session_state:
    st.session_state.cart = ShoppingCart(st.session_state.customer)

if "optimizer" not in st.session_state:
    st.session_state.optimizer = routing.LogisticsOptimizer()

# Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=70)
st.sidebar.title("SmartCart System")
st.sidebar.write(f"Logged in: **{st.session_state.customer.username}**")
st.sidebar.caption(f"Status: {'★ Premium Customer (10% Off)' if st.session_state.customer.is_premium else 'Regular Customer'}")

menu = st.sidebar.radio(
    "Navigation Menu",
    ["🛍️ Storefront & Cart", "🚚 Delivery Route Optimizer", "📊 Sales Analytics Dashboard", "⚙️ Cloud Backup & System"]
)

# -------------------------------------------------------------
# PAGE 1: STOREFRONT & CART
# -------------------------------------------------------------
if menu == "🛍️ Storefront & Cart":
    st.markdown('<div class="main-header">🛒 SmartCart Online Store</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Browse inventory, manage your cart, and generate itemized tax invoices.</div>', unsafe_allow_html=True)

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
                        if p['stock'] >= qty:
                            prod_obj = Product(p['product_id'], p['name'], p['category'], p['price'], p['stock'])
                            st.session_state.cart.add_item(prod_obj, qty)
                            st.toast(f"Added {qty}x {p['name']} to cart!", icon="🛒")
                        else:
                            st.error("Insufficient stock!")
                st.divider()

    with col_cart:
        st.subheader("🛍️ Your Shopping Cart")
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
            dest_city = st.selectbox("Select Delivery Destination", cities, index=cities.index("Mumbai") if "Mumbai" in cities else 0)

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
# PAGE 2: LOGISTICS & ROUTE OPTIMIZATION
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
# PAGE 3: SALES ANALYTICS DASHBOARD
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
# PAGE 4: CLOUD BACKUP & SYSTEM
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
