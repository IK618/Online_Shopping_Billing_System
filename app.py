"""
app.py
Streamlit Web Frontend for Online Shopping & Billing System
SmartCart Retail & Logistics Management Platform
Features:
  - Custom Dark-Slate Design System (#0B0F19, #131C2E, #222F43)
  - Mission Control Layout & High-Density Telemetry Cards
  - Live Fleet Dispatch Feed & Geographically Accurate Dijkstra Corridors
  - 3D Interactive OpenStreetMap / PyDeck Delivery GPS Tracking
  - Executive Business Intelligence Analytics (NumPy + Matplotlib)
  - Luxury Dark E-Commerce Storefront & Instant Invoicing
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
    page_title="SmartCart // Retail & Logistics Engine",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# SMARTCART DESIGN SYSTEM & CUSTOM THEME INJECTION
# -------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }
    
    /* Dark Theme Surface Backgrounds */
    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
    }

    [data-testid="stSidebar"] {
        background-color: #0E131F !important;
        border-right: 1px solid #1E293B;
    }

    /* SmartCart Mission Control Header */
    .sc-hero {
        background: linear-gradient(135deg, #0F172A 0%, #131C2E 60%, #1E293B 100%);
        border: 1px solid #222F43;
        border-left: 4px solid #38BDF8;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.6rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .sc-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #38BDF8;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    .sc-title {
        font-size: 1.9rem;
        font-weight: 800;
        color: #F8FAFC;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .sc-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        margin-top: 0.3rem;
    }

    /* SmartCart Telemetry Cards */
    .sc-card {
        background-color: #131C2E;
        border: 1px solid #222F43;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .sc-card:hover {
        border-color: #38BDF8;
        transform: translateY(-2px);
    }

    /* Metric Cards */
    .metric-box {
        background-color: #131C2E;
        border: 1px solid #222F43;
        border-radius: 8px;
        padding: 1rem 1.2rem;
    }
    .metric-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .metric-val {
        font-size: 1.65rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-top: 0.2rem;
    }
    .metric-delta {
        font-size: 0.75rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }
    .delta-green { color: #10B981; }
    .delta-blue { color: #38BDF8; }

    /* Badges & Status Pills */
    .pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
    }
    .pill-green { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .pill-blue { background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .pill-amber { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .pill-red { background: rgba(244, 63, 94, 0.15); color: #FB7185; border: 1px solid rgba(244, 63, 94, 0.3); }

    /* Store Product Cards */
    .store-card {
        background-color: #131C2E;
        border: 1px solid #222F43;
        border-radius: 10px;
        padding: 1.1rem;
        margin-bottom: 0.9rem;
    }
    .store-card:hover {
        border-color: #38BDF8;
    }
    .price-display {
        font-size: 1.35rem;
        font-weight: 800;
        color: #38BDF8;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Live Fleet Feed Item */
    .feed-item {
        background: #0E1422;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.7rem;
    }
    .feed-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .feed-desc {
        font-size: 0.78rem;
        color: #94A3B8;
        margin-top: 0.2rem;
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

if "optimizer" not in st.session_state or not hasattr(st.session_state.optimizer, "interpolate_delivery_gps"):
    st.session_state.optimizer = routing.LogisticsOptimizer()

# -------------------------------------------------------------
# SIDEBAR NAVIGATION & AUTHENTICATION
# -------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sc-tag">SMARTCART FLEET OS // v2.6</div>', unsafe_allow_html=True)
    st.markdown("## **SmartCart** Logistics")
    st.caption("Central Operations & Commerce Hub")
    st.divider()

    # User Profile / Login Card
    if st.session_state.auth_user is None:
        st.markdown("#### 🔐 Access Gateway")
        auth_mode = st.radio("Mode", ["Sign In", "Register"], horizontal=True, label_visibility="collapsed")

        if auth_mode == "Sign In":
            l_user = st.text_input("Username", key="l_user", placeholder="Enter username")
            l_pass = st.text_input("Password", type="password", key="l_pass", placeholder="••••••••")

            if st.button("Authenticate ➔", type="primary", use_container_width=True):
                user_row = database.authenticate_user(l_user, l_pass)
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
                    st.success(f"Access granted: {user_row['username']}")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

            st.markdown("---")
            st.caption("⚡ **Demo Access Profiles:**")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if st.button("Customer (Buyer)", use_container_width=True):
                    u = database.authenticate_user("rahul_sharma", "pass123")
                    st.session_state.auth_user = dict(u)
                    st.session_state.customer = Customer(u["user_id"], u["username"], u["email"], u["city"], bool(u["is_premium"]))
                    st.session_state.cart = ShoppingCart(st.session_state.customer)
                    st.rerun()
            with col_d2:
                if st.button("Admin (Seller)", use_container_width=True):
                    u = database.authenticate_user("admin_user", "admin123")
                    st.session_state.auth_user = dict(u)
                    st.session_state.customer = None
                    st.session_state.cart = None
                    st.rerun()

        else:
            st.markdown("#### 📝 Register Identity")
            reg_u = st.text_input("Username", key="r_u")
            reg_e = st.text_input("Email", key="r_e")
            reg_p = st.text_input("Password", type="password", key="r_p")
            cities = st.session_state.optimizer.get_all_cities()
            reg_c = st.selectbox("Operating Hub", cities, key="r_c")
            reg_prem = st.checkbox("Sign as Premium Customer (10% Off)", value=True)

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
            st.markdown('<span class="pill pill-green">● STORE SELLER (ADMIN)</span>', unsafe_allow_html=True)
        else:
            tier_badge = "● PREMIUM TIER (10% OFF)" if user_info.get("is_premium") else "● REGULAR TIER (2% OFF)"
            st.markdown(f'<span class="pill pill-blue">{tier_badge}</span>', unsafe_allow_html=True)
        st.write(f"📍 Node: **{user_info.get('city', 'Bengaluru')}**")

        if st.button("🚪 Terminate Session", use_container_width=True):
            st.session_state.auth_user = None
            st.session_state.customer = None
            st.session_state.cart = None
            st.rerun()

    st.divider()

    # Navigation Menu
    user_role = st.session_state.auth_user["role"] if st.session_state.auth_user else "guest"
    if user_role == "admin":
        menu = st.radio(
            "Operations Console",
            ["🚚 Delivery Route & Fleet Telemetry", "📊 Business Intelligence & KPIs", "🛠️ Warehouse Inventory Hub", "⚙️ Cloud Archival & Services"]
        )
    else:
        menu = st.radio(
            "Customer Terminal",
            ["🛍️ Catalog & Cart Checkout", "🚚 Delivery Route & Fleet Telemetry", "📊 Business Intelligence & KPIs", "⚙️ Cloud Archival & Services"]
        )

# -------------------------------------------------------------
# TAB 1: DELIVERY ROUTE & FLEET TELEMETRY
# -------------------------------------------------------------
if menu == "🚚 Delivery Route & Fleet Telemetry":
    st.markdown("""
        <div class="sc-hero">
            <div class="sc-tag">SATELLITE TELEMETRY // REAL-TIME DISPATCH CORRIDORS</div>
            <h1 class="sc-title">Logistics Command Center & Graph Pathfinding</h1>
            <div class="sc-subtitle">Real-time shortest path optimization powered by SciPy Dijkstra on sparse CSR matrices and NetworkX network topology.</div>
        </div>
    """, unsafe_allow_html=True)

    optimizer = st.session_state.optimizer
    cities = optimizer.get_all_cities()

    # TOP: EXECUTIVE KPI CARDS
    target_city = st.selectbox("Target Delivery Hub", cities, index=cities.index("Delhi") if "Delhi" in cities else 0)
    path, distance = optimizer.find_shortest_route(target_city)

    est_days = round(distance / 650.0, 1)
    fuel_burn = round(distance * 0.32, 1)
    co2_footprint = round(distance * 0.85, 1)

    t_col1, t_col2, t_col3, t_col4 = st.columns(4)
    with t_col1:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">🛣️ Highway Distance</div>
                <div class="metric-val">{distance:,.0f} <span style="font-size:1rem;color:#94A3B8;">km</span></div>
                <div class="metric-delta delta-green">Dijkstra Solved</div>
            </div>
        """, unsafe_allow_html=True)
    with t_col2:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">⏱️ Estimated Transit Window</div>
                <div class="metric-val">{est_days} <span style="font-size:1rem;color:#94A3B8;">days</span></div>
                <div class="metric-delta delta-blue">650 km / day transit</div>
            </div>
        """, unsafe_allow_html=True)
    with t_col3:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">🏢 Corridor Waypoints</div>
                <div class="metric-val">{len(path)} <span style="font-size:1rem;color:#94A3B8;">hubs</span></div>
                <div class="metric-delta delta-green">Zero Bottlenecks</div>
            </div>
        """, unsafe_allow_html=True)
    with t_col4:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">⛽ Heavy Freight Fuel</div>
                <div class="metric-val">{fuel_burn:,.0f} <span style="font-size:1rem;color:#94A3B8;">L</span></div>
                <div class="metric-delta delta-blue">{co2_footprint:,.0f} kg CO2 est.</div>
            </div>
        """, unsafe_allow_html=True)

    # MAP MODE TOGGLE & LIVE DRIVER TELEMETRY
    mode_c1, mode_c2 = st.columns([1.5, 1])
    with mode_c1:
        map_mode = st.radio(
            "Visualization Engine",
            ["🗺️ 3D Interactive OpenStreetMap GPS Tracker (Live Vehicle Pin)", "🛰️ Static Network Topology Graph (Matplotlib)"],
            horizontal=True
        )
    with mode_c2:
        st.write("")

    # LIVE DRIVER PROGRESS CONTROLS
    st.markdown("#### 📍 Live Delivery Driver GPS Telemetry Simulator")
    sim_c1, sim_c2 = st.columns([2, 1], gap="medium")
    with sim_c1:
        prog_pct = st.slider(
            "Simulate Driver Highway Transit Progress",
            min_value=0,
            max_value=100,
            value=45,
            step=5,
            help="Drag slider to simulate vehicle moving in real-time between Dijkstra hubs"
        )
    with sim_c2:
        st.write("")
        if prog_pct == 100:
            st.markdown('<span class="pill pill-green" style="font-size:0.9rem;">🏁 ORDER DELIVERED TO CUSTOMER</span>', unsafe_allow_html=True)
        elif prog_pct == 0:
            st.markdown('<span class="pill pill-amber" style="font-size:0.9rem;">📦 DOCKED AT BENGALURU WAREHOUSE</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="pill pill-blue" style="font-size:0.9rem;">🚛 IN TRANSIT ({prog_pct}% COMPLETE)</span>', unsafe_allow_html=True)

    # Compute live interpolated GPS coordinates
    driver_lat, driver_lon, seg_name, curr_speed, next_hub = optimizer.interpolate_delivery_gps(path, prog_pct / 100.0)

    # MAIN BODY: MAP & DRIVER PROFILE / ACTIVE FLEET TELEMETRY
    map_col, fleet_col = st.columns([2.3, 1.2], gap="large")

    with map_col:
        if "3D Interactive" in map_mode:
            st.markdown(f"##### 🗺️ 3D Interactive Satellite Map — Live Vehicle Pin at `[{driver_lat:.4f}° N, {driver_lon:.4f}° E]`")
            deck = optimizer.create_interactive_deck(path, driver_lat, driver_lon, target_city)
            st.pydeck_chart(deck, use_container_width=True)
            st.caption("💡 **Tip:** Click and drag to pan across highways, use mouse scroll to zoom into cities, and hold right-click to tilt in 3D!")
        else:
            st.markdown("##### 🛰️ Network Topology Distribution Graph (Matplotlib)")
            fig = optimizer.generate_route_plot(highlighted_path=path)
            st.pyplot(fig)

    with fleet_col:
        st.markdown("#### 👤 Assigned Delivery Personnel")
        st.markdown(f"""
            <div class="sc-card" style="border-left: 3px solid #10B981;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:800; font-size:1.05rem; color:#F8FAFC;">Vikram Singh</span>
                    <span class="pill pill-green">ACTIVE DRIVER</span>
                </div>
                <div style="font-size:0.8rem; color:#94A3B8; margin-top:0.2rem;">Driver ID: <code>DRV-8821</code> | Rating: ⭐ 4.9 (1,420 drops)</div>
                <div style="font-size:0.8rem; color:#94A3B8;">Vehicle: <b>Tata Ace EV Van (#KA-05-EV-4421)</b></div>
                <hr style="border-color:#222F43; margin:0.6rem 0;" />
                <div style="font-size:0.82rem; color:#CBD5E1;">
                    📍 <b>Current Highway:</b> <span style="color:#38BDF8;">{seg_name}</span><br>
                    ⚡ <b>Telemetry Velocity:</b> <span style="color:#10B981;">{curr_speed} km/h</span><br>
                    🎯 <b>Next Waypoint:</b> <span style="color:#F59E0B;">{next_hub}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 📡 Regional Fleet Telemetry")
        st.markdown("""
            <div class="feed-item" style="border-left:3px solid #38BDF8;">
                <div style="display:flex; justify-content:space-between;">
                    <span class="feed-title">🚛 UNIT #MH-4109</span>
                    <span class="pill pill-blue">IN TRANSIT</span>
                </div>
                <div class="feed-desc">Mumbai ➔ Pune ➔ Bengaluru | 92% Capacity</div>
                <div style="font-size:0.75rem; color:#94A3B8; margin-top:0.3rem;">On Schedule (ETA: 4h 30m)</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="feed-item" style="border-left:3px solid #F59E0B;">
                <div style="display:flex; justify-content:space-between;">
                    <span class="feed-title">🚛 UNIT #DL-1092</span>
                    <span class="pill pill-amber">DISPATCH QUEUED</span>
                </div>
                <div class="feed-desc">Delhi ➔ Jaipur ➔ Ahmedabad | Awaiting Cargo Seal</div>
                <div style="font-size:0.75rem; color:#FBBF24; margin-top:0.3rem;">Dock 04 Loading</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("##### 📍 Active Corridor Route")
        st.info(" ➔ ".join(path))

# -------------------------------------------------------------
# TAB 2: STOREFRONT & CART CHECKOUT
# -------------------------------------------------------------
elif menu == "🛍️ Catalog & Cart Checkout":
    st.markdown("""
        <div class="sc-hero">
            <div class="sc-tag">SMARTCART RETAIL // E-COMMERCE ENGINE</div>
            <h1 class="sc-title">Curated Inventory & Automated Billing</h1>
            <div class="sc-subtitle">Browse products with real-time stock control, dynamic customer tier discounts, and instant tax invoicing.</div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.auth_user is None:
        st.info("💡 You are browsing in guest mode. Use the sidebar to sign in or click **Customer** to test instant checkout.")

    col_catalog, col_cart = st.columns([3, 2], gap="large")

    with col_catalog:
        st.markdown("#### 📦 Product Catalog")

        f_col1, f_col2, f_col3 = st.columns([2, 1.5, 1.5])
        with f_col1:
            search_query = st.text_input("Search", placeholder="🔍 Search by name...", label_visibility="collapsed")
        with f_col2:
            categories = ["All", "Electronics", "Furniture", "Home & Kitchen", "Fashion", "Groceries"]
            cat_choice = st.selectbox("Category", categories, label_visibility="collapsed")
        with f_col3:
            sort_choice = st.selectbox("Sort", ["Price: Low to High", "Price: High to Low", "Name: A-Z"], label_visibility="collapsed")

        raw_products = database.get_all_products(cat_choice if cat_choice != "All" else None)
        products_list = [dict(p) for p in raw_products]

        if search_query.strip():
            products_list = [p for p in products_list if search_query.lower() in p["name"].lower() or search_query.lower() in p["category"].lower()]

        if sort_choice == "Price: Low to High":
            products_list.sort(key=lambda x: x["price"])
        elif sort_choice == "Price: High to Low":
            products_list.sort(key=lambda x: x["price"], reverse=True)
        elif sort_choice == "Name: A-Z":
            products_list.sort(key=lambda x: x["name"])

        for p in products_list:
            stock_pill = f'<span class="pill pill-green">✓ IN STOCK ({p["stock"]})</span>' if p['stock'] > 5 else (f'<span class="pill pill-amber">⚠️ LOW STOCK ({p["stock"]})</span>' if p['stock'] > 0 else '<span class="pill pill-red">✕ OUT OF STOCK</span>')

            st.markdown(f"""
                <div class="store-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="pill pill-blue">{p['category']}</span>
                        {stock_pill}
                    </div>
                    <div style="font-size:1.15rem; font-weight:700; color:#F8FAFC; margin:0.4rem 0 0.2rem 0;">{p['name']}</div>
                    <div class="price-display">₹{p['price']:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)

            c_qty, c_btn = st.columns([1, 2])
            with c_qty:
                qty = st.number_input("Qty", min_value=1, max_value=max(1, p['stock']), value=1, key=f"q_{p['product_id']}", label_visibility="collapsed")
            with c_btn:
                if st.button("🛒 Add to Order", key=f"b_{p['product_id']}", use_container_width=True, disabled=(p['stock'] <= 0)):
                    if st.session_state.customer is None:
                        st.error("Please sign in from the sidebar to purchase.")
                    else:
                        prod_obj = Product(p['product_id'], p['name'], p['category'], p['price'], p['stock'])
                        st.session_state.cart.add_item(prod_obj, qty)
                        st.toast(f"Added {qty}x {p['name']} to order!", icon="📦")
            st.write("")

    with col_cart:
        st.markdown("#### 🛒 Active Dispatch Order")

        if st.session_state.cart is None:
            st.markdown("""
                <div class="sc-card" style="text-align:center; padding:2.5rem 1rem;">
                    <div style="font-size:2.5rem; margin-bottom:0.5rem;">🔐</div>
                    <div style="font-weight:700; color:#F8FAFC;">Authentication Required</div>
                    <p style="color:#94A3B8; font-size:0.85rem;">Sign in as a customer from the left sidebar to start building your cart.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            cart = st.session_state.cart
            if len(cart) == 0:
                st.markdown("""
                    <div class="sc-card" style="text-align:center; padding:2rem 1rem;">
                        <div style="font-size:2rem; margin-bottom:0.3rem;">🛒</div>
                        <div style="font-weight:700; color:#CBD5E1;">Your cart is empty</div>
                        <p style="color:#94A3B8; font-size:0.85rem;">Select items from the catalog to prepare your bill.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                cart_display = []
                for item in cart.iter_items():
                    cart_display.append({
                        "Item": item.product.name[:25] + ("..." if len(item.product.name) > 25 else ""),
                        "Qty": item.quantity,
                        "Rate": f"₹{item.product.price:,.2f}",
                        "Total": f"₹{item.total_price:,.2f}"
                    })
                st.dataframe(pd.DataFrame(cart_display), use_container_width=True, hide_index=True)

                totals = cart.calculate_totals()
                disc_rate = int(totals['discount_rate'] * 100)

                st.markdown(f"""
                    <div class="sc-card">
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem; color:#94A3B8;">
                            <span>Subtotal:</span><span>₹{totals['subtotal']:,.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem; color:#34D399;">
                            <span>Customer Discount ({disc_rate}%):</span><span>-₹{totals['discount_amount']:,.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem; color:#94A3B8;">
                            <span>GST Tax (5%):</span><span>₹{totals['tax']:,.2f}</span>
                        </div>
                        <hr style="border-color:#222F43; margin:0.5rem 0;" />
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:700; color:#F8FAFC;">Total Payable:</span>
                            <span style="font-size:1.45rem; font-weight:800; color:#38BDF8; font-family:'JetBrains Mono';">₹{totals['total']:,.2f}</span>
                        </div>
                        <div style="font-size:0.75rem; color:#64748B; text-align:right; margin-top:0.2rem;">
                            Banker's rounded cash integer: ₹{totals['integer_rupees']:,}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                cities = st.session_state.optimizer.get_all_cities()
                dest_city = st.selectbox("Destination Hub", cities, index=cities.index(st.session_state.customer.city) if st.session_state.customer.city in cities else 0)

                b1, b2 = st.columns([2, 1])
                with b1:
                    if st.button("💳 Generate Invoice & Dispatch", type="primary", use_container_width=True):
                        cart_items_data = [
                            {"product_id": item.product.product_id, "name": item.product.name, "quantity": item.quantity, "unit_price": item.product.price, "total_price": item.total_price}
                            for item in cart.iter_items()
                        ]

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

                        receipt_text = billing.generate_text_receipt(order_id, st.session_state.customer.username, dest_city, cart_items_data, totals)
                        csv_path = billing.export_order_to_csv(order_id, st.session_state.customer.username, dest_city, cart_items_data, totals)
                        billing.send_invoice_email(st.session_state.customer.email, order_id, receipt_text)

                        st.balloons()
                        st.success(f"Order #{order_id} Confirmed! Invoiced & Queued for Freight.")

                        with open(csv_path, "r") as f:
                            st.download_button(
                                label="📥 Download Official CSV Tax Invoice",
                                data=f.read(),
                                file_name=f"smartcart_invoice_{order_id}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )

                        with st.expander("📄 View Formatted ASCII Receipt", expanded=True):
                            st.code(receipt_text, language="text")

                        st.session_state.cart.clear()

                with b2:
                    if st.button("Clear Order", use_container_width=True):
                        st.session_state.cart.clear()
                        st.rerun()

# -------------------------------------------------------------
# TAB 3: BUSINESS INTELLIGENCE & REVENUE ANALYTICS
# -------------------------------------------------------------
elif menu == "📊 Business Intelligence & KPIs":
    st.markdown("""
        <div class="sc-hero">
            <div class="sc-tag">EXECUTIVE METRICS // NUMPY HIGH-PERFORMANCE COMPUTATION</div>
            <h1 class="sc-title">Revenue & Fleet Business Intelligence</h1>
            <div class="sc-subtitle">Real-time financial telemetry calculated via NumPy multidimensional array vectorization.</div>
        </div>
    """, unsafe_allow_html=True)

    metrics = analytics.compute_sales_metrics()

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Total Store Revenue</div>
                <div class="metric-val">₹{metrics['total_revenue']:,.2f}</div>
                <div class="metric-delta delta-green">↑ 14.2% MoM Velocity</div>
            </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Average Order Value</div>
                <div class="metric-val">₹{metrics['average_order_value']:,.2f}</div>
                <div class="metric-delta delta-blue">↑ 5.8% Quality Index</div>
            </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Peak Transaction Ticket</div>
                <div class="metric-val">₹{metrics['max_order_value']:,.2f}</div>
                <div class="metric-delta delta-green">Highest Cart Recorded</div>
            </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Completed Transactions</div>
                <div class="metric-val">{metrics['order_count']} <span style="font-size:0.9rem;color:#94A3B8;">orders</span></div>
                <div class="metric-delta delta-blue">ACID Logged in SQLite</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 📈 Revenue Trajectory & Volume Distribution")
    fig = analytics.generate_sales_dashboard()
    st.pyplot(fig)

    st.write("")
    st.markdown("#### 📋 Real-Time SQLite Transaction Ledger")
    recent_orders = database.get_order_history(limit=15)
    if recent_orders:
        order_table = [
            {
                "Order ID": f"#{o['order_id']}",
                "Timestamp": o['order_date'],
                "Customer": o['username'],
                "Destination": o['delivery_city'],
                "Net Total": f"₹{o['total']:,.2f}",
                "Status": "🟢 " + o['status']
            }
            for o in recent_orders
        ]
        st.dataframe(pd.DataFrame(order_table), use_container_width=True, hide_index=True)
    else:
        st.info("No transaction logs recorded yet.")

# -------------------------------------------------------------
# TAB 4: WAREHOUSE INVENTORY HUB (ADMIN)
# -------------------------------------------------------------
elif menu == "🛠️ Warehouse Inventory Hub":
    st.markdown("""
        <div class="sc-hero">
            <div class="sc-tag">WAREHOUSE INVENTORY // SKU MANAGEMENT</div>
            <h1 class="sc-title">Stock Logistics & Inventory Replenishment</h1>
            <div class="sc-subtitle">Real-time asset valuation, SKU catalog modifications, and stock reorder controls.</div>
        </div>
    """, unsafe_allow_html=True)

    tab_inv, tab_add, tab_edit = st.tabs(["📋 Inventory Valuation", "➕ Register New SKU", "⚙️ Restock & Adjust Prices"])

    with tab_inv:
        all_prods = database.get_all_products()
        total_skus = len(all_prods)
        total_units = sum(p["stock"] for p in all_prods)
        inventory_val = sum(p["price"] * p["stock"] for p in all_prods)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Active SKUs</div>
                    <div class="metric-val">{total_skus}</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Units in Warehouse</div>
                    <div class="metric-val">{total_units:,}</div>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Total Inventory Valuation</div>
                    <div class="metric-val">₹{inventory_val:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)

        st.write("")
        prod_table = [
            {"SKU": f"#{p['product_id']}", "Product Name": p["name"], "Category": p["category"], "Unit Price": f"₹{p['price']:,.2f}", "Units in Stock": p["stock"]}
            for p in all_prods
        ]
        st.dataframe(pd.DataFrame(prod_table), use_container_width=True, hide_index=True)

    with tab_add:
        st.markdown("##### ➕ Register New Product SKU")
        with st.form("new_sku_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                p_name = st.text_input("Product Title", placeholder="e.g. Mechanical Switch Keyboard")
                p_cat = st.selectbox("Category", ["Electronics", "Furniture", "Home & Kitchen", "Fashion", "Groceries", "Sports"])
            with col_b:
                p_price = st.number_input("Retail Price (₹)", min_value=1.0, value=1999.0, step=50.0)
                p_stock = st.number_input("Initial Warehouse Stock", min_value=1, value=30, step=5)

            if st.form_submit_button("Commit to Inventory", type="primary"):
                if p_name.strip():
                    new_id = database.add_product(p_name, p_cat, p_price, p_stock)
                    st.success(f"SKU #{new_id} ('{p_name}') registered into SQLite!")
                else:
                    st.error("Title cannot be empty.")

    with tab_edit:
        st.markdown("##### ⚙️ Adjust Price & Replenish Stock")
        all_prods = database.get_all_products()
        prod_dict = {f"#{p['product_id']} — {p['name']} (Stock: {p['stock']})": p for p in all_prods}

        chosen_key = st.selectbox("Select SKU to Edit", list(prod_dict.keys()))
        selected_p = prod_dict[chosen_key]

        col_u1, col_u2, col_u3 = st.columns(3)
        with col_u1:
            u_price = st.number_input("Adjust Price (₹)", min_value=1.0, value=float(selected_p["price"]), step=50.0)
        with col_u2:
            u_stock = st.number_input("Adjust Stock Quantity", min_value=0, value=int(selected_p["stock"]), step=5)
        with col_u3:
            st.write("")
            st.write("")
            if st.button("Apply Updates", type="primary", use_container_width=True):
                database.update_product_details(selected_p["product_id"], u_price, u_stock)
                st.success(f"SKU #{selected_p['product_id']} updated!")
                st.rerun()

        st.divider()
        if st.button("🗑️ Delete SKU from Catalog"):
            database.delete_product(selected_p["product_id"])
            st.warning(f"SKU #{selected_p['product_id']} removed.")
            st.rerun()

# -------------------------------------------------------------
# TAB 5: CLOUD ARCHIVAL & SYSTEM SERVICES
# -------------------------------------------------------------
elif menu == "⚙️ Cloud Archival & Services":
    st.markdown("""
        <div class="sc-hero">
            <div class="sc-tag">CONCURRENCY & NETWORKING // THREADING + FTP + SOCKETS</div>
            <h1 class="sc-title">Cloud Infrastructure & POS Network Gateway</h1>
            <div class="sc-subtitle">Background daemon threads, automated FTP archival, and low-level TCP socket listeners.</div>
        </div>
    """, unsafe_allow_html=True)

    b1, b2 = st.columns(2, gap="large")
    with b1:
        st.markdown("#### ☁️ Asynchronous Database Archival")
        st.write("Spawns a background thread (`threading.Thread`) that transmits an encrypted database snapshot over FTP (`ftplib`) without stalling UI telemetry.")
        if st.button("🚀 Trigger Cloud Backup Now", type="primary"):
            thread = backup_service.run_async_backup()
            st.success("Background worker thread dispatched! SQLite snapshot transmitted via FTP.")

    with b2:
        st.markdown("#### 🔌 POS Cashier TCP Sockets")
        st.write("Connects local terminal cashiers over TCP sockets (`AF_INET`, `SOCK_STREAM`) on port `65432`.")
        st.code("""
# Launch TCP Server in your terminal:
python network_pos.py
        """, language="bash")
