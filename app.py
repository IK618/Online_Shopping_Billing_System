"""
app.py
Streamlit Web Frontend for Online Shopping & Billing System
SmartCart Autonomous Retail & Logistics Management Platform

Features:
  - Dual-Theme System: Futuristic Cyber-Dark (#0B0F19) & Clean Apple-Inspired Light (#F8FAFC)
  - Sticky Frosted-Glass Top Navigation & Scroll Progress Bar
  - Accessibility Skip-to-Content Anchor
  - Global Cross-Category Site Search
  - Password Visibility Show/Hide Toggles
  - Dismissible Privacy Cookie Consent Banner
  - Confirmation Modals via @st.dialog (Checkout & SKU Deletion)
  - 3D CSS Perspective Tilt & Micro-Interaction Hover States
  - Dedicated @media print Stylesheet for Paper/PDF Invoicing
  - UTM Marketing Telemetry Capture & Reporting
  - Form Success / Error State Feedback with Animations
  - Expandable FAQ Accordion Section
  - Floating 24/7 Support Desk Dialog & Back-to-Top Navigation
  - Dynamic Last Updated Timestamp & Real-Time Fleet Status Footer
  - 3D WebGL / OpenStreetMap Interactive Delivery GPS Tracker (PyDeck)
  - SciPy Sparse CSR Dijkstra Shortest-Path Optimizer & NetworkX Topology
  - Executive Business Intelligence Analytics (NumPy Vectorization + Matplotlib)
  - Role-Based Authentication (Buyer vs Seller / Merchant)
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

# -------------------------------------------------------------
# 1. PAGE SETUP & SESSION STATE INITIALIZATION
# -------------------------------------------------------------
st.set_page_config(
    page_title="SmartCart // Retail & Logistics Engine",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "auth_user" not in st.session_state:
    st.session_state.auth_user = None

if "customer" not in st.session_state:
    st.session_state.customer = None

if "cart" not in st.session_state:
    st.session_state.cart = None

if "cookies_accepted" not in st.session_state:
    st.session_state.cookies_accepted = False

if "global_search" not in st.session_state:
    st.session_state.global_search = ""

if "trigger_print" not in st.session_state:
    st.session_state.trigger_print = False

if "optimizer" not in st.session_state or not hasattr(st.session_state.optimizer, "interpolate_delivery_gps"):
    st.session_state.optimizer = routing.LogisticsOptimizer()

# Capture UTM Marketing Parameters from URL Query
if "utm_params" not in st.session_state:
    st.session_state.utm_params = {
        "source": st.query_params.get("utm_source", "direct / organic"),
        "medium": st.query_params.get("utm_medium", "none"),
        "campaign": st.query_params.get("utm_campaign", "autonomous_retail_launch"),
        "term": st.query_params.get("utm_term", "scipy_dijkstra_delivery"),
    }

# -------------------------------------------------------------
# 2. DYNAMIC DUAL-THEME STYLESHEET & ACCESSIBILITY INJECTION
# -------------------------------------------------------------
is_dark = (st.session_state.theme == "dark")

if is_dark:
    bg_app = "#0B0F19"
    bg_sidebar = "#0E131F"
    bg_card = "#131C2E"
    border_card = "#222F43"
    text_primary = "#F8FAFC"
    text_secondary = "#94A3B8"
    accent_blue = "#38BDF8"
    accent_glow = "rgba(56, 189, 248, 0.22)"
    hero_gradient = "linear-gradient(135deg, #0F172A 0%, #131C2E 60%, #1E293B 100%)"
    feed_bg = "#0E1422"
    nav_glass = "rgba(11, 15, 25, 0.85)"
    cookie_bg = "#131C2E"
else:
    # Apple-Inspired Clean Light Mode
    bg_app = "#F8FAFC"
    bg_sidebar = "#FFFFFF"
    bg_card = "#FFFFFF"
    border_card = "#E2E8F0"
    text_primary = "#0F172A"
    text_secondary = "#64748B"
    accent_blue = "#2563EB"
    accent_glow = "rgba(37, 99, 235, 0.15)"
    hero_gradient = "linear-gradient(135deg, #EFF6FF 0%, #F8FAFC 60%, #E2E8F0 100%)"
    feed_bg = "#F1F5F9"
    nav_glass = "rgba(255, 255, 255, 0.88)"
    cookie_bg = "#FFFFFF"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        scroll-behavior: smooth;
    }}
    
    /* Accessibility: Skip to main content link */
    .skip-to-content {{
        position: absolute;
        top: -60px;
        left: 15px;
        background: {accent_blue};
        color: #FFFFFF !important;
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: 700;
        z-index: 1000000;
        transition: top 0.2s ease;
        text-decoration: none;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    }}
    .skip-to-content:focus {{
        top: 15px;
    }}

    /* Top Scroll Progress Line */
    #scroll-progress-line {{
        position: fixed;
        top: 0;
        left: 0;
        height: 3.5px;
        width: 0%;
        background: linear-gradient(90deg, #38BDF8, #6366F1, #10B981);
        z-index: 999999;
        transition: width 0.1s ease-out;
    }}

    /* Global App Canvas */
    .stApp {{
        background-color: {bg_app} !important;
        color: {text_primary} !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: {bg_sidebar} !important;
        border-right: 1px solid {border_card} !important;
    }}

    /* Sticky Frosted Header Navbar */
    .sticky-navbar {{
        position: sticky;
        top: 0;
        z-index: 999;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        background: {nav_glass};
        border-bottom: 1px solid {border_card};
        padding: 0.75rem 1.25rem;
        margin: -1.5rem -1rem 1.5rem -1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 0 0 14px 14px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }}

    /* Mission Control Hero Banner */
    .sc-hero {{
        background: {hero_gradient};
        border: 1px solid {border_card};
        border-left: 4px solid {accent_blue};
        padding: 1.5rem 2rem;
        border-radius: 14px;
        margin-bottom: 1.6rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        transition: transform 0.3s ease;
    }}
    .sc-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: {accent_blue};
        font-weight: 700;
        margin-bottom: 0.3rem;
    }}
    .sc-title {{
        font-size: 1.85rem;
        font-weight: 800;
        color: {text_primary};
        margin: 0;
        letter-spacing: -0.02em;
    }}
    .sc-subtitle {{
        font-size: 0.92rem;
        color: {text_secondary};
        margin-top: 0.35rem;
    }}

    /* 3D Perspective Cards & Micro-Interactions */
    .sc-card, .store-card, .metric-box {{
        background-color: {bg_card} !important;
        border: 1px solid {border_card} !important;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.25s ease, border-color 0.25s ease !important;
        transform-style: preserve-3d;
        perspective: 1000px;
    }}
    .sc-card:hover, .store-card:hover, .metric-box:hover {{
        border-color: {accent_blue} !important;
        transform: translateY(-5px) scale(1.012) !important;
        box-shadow: 0 14px 30px {accent_glow} !important;
    }}

    /* Metric Counters */
    .metric-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: {text_secondary};
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }}
    .metric-val {{
        font-size: 1.65rem;
        font-weight: 800;
        color: {text_primary};
        margin-top: 0.2rem;
    }}
    .metric-delta {{
        font-size: 0.75rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }}
    .delta-green {{ color: #10B981; }}
    .delta-blue {{ color: {accent_blue}; }}

    /* Status Pills */
    .pill {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
    }}
    .pill-green {{ background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.35); }}
    .pill-blue {{ background: rgba(56, 189, 248, 0.15); color: {accent_blue}; border: 1px solid rgba(56, 189, 248, 0.35); }}
    .pill-amber {{ background: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.35); }}
    .pill-red {{ background: rgba(244, 63, 94, 0.15); color: #F43F5E; border: 1px solid rgba(244, 63, 94, 0.35); }}

    /* Pricing Display */
    .price-display {{
        font-size: 1.35rem;
        font-weight: 800;
        color: {accent_blue};
        font-family: 'JetBrains Mono', monospace;
    }}

    /* Live Fleet Feed Item */
    .feed-item {{
        background: {feed_bg};
        border: 1px solid {border_card};
        border-radius: 8px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.7rem;
        transition: border-color 0.2s;
    }}
    .feed-item:hover {{
        border-color: {accent_blue};
    }}
    .feed-title {{
        font-size: 0.9rem;
        font-weight: 700;
        color: {text_primary};
    }}
    .feed-desc {{
        font-size: 0.78rem;
        color: {text_secondary};
        margin-top: 0.2rem;
    }}

    /* Form Feedback States & Micro-Animations */
    @keyframes shake {{
        0%, 100% {{ transform: translateX(0); }}
        20%, 60% {{ transform: translateX(-6px); }}
        40%, 80% {{ transform: translateX(6px); }}
    }}
    .form-error-shake {{
        animation: shake 0.35s ease-in-out;
    }}
    .form-success-card {{
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
    }}
    .form-error-card {{
        background: rgba(244, 63, 94, 0.1);
        border: 1px solid rgba(244, 63, 94, 0.4);
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
    }}

    /* Status Pulse Animation */
    @keyframes pulse-dot {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.4; transform: scale(0.9); }}
    }}
    .status-pulse {{
        color: #10B981;
        display: inline-block;
        animation: pulse-dot 2s infinite ease-in-out;
    }}

    /* Cookie Banner Container */
    .cookie-banner-box {{
        background-color: {cookie_bg};
        border: 1px solid {border_card};
        border-radius: 12px;
        padding: 1rem 1.4rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }}

    /* Site Footer */
    .site-footer {{
        border-top: 1px solid {border_card};
        padding: 1.5rem 0.5rem;
        margin-top: 3rem;
        font-size: 0.85rem;
        color: {text_secondary};
    }}

    /* Responsive Mobile Layout Adjustments */
    @media (max-width: 768px) {{
        .sc-hero {{
            padding: 1.1rem 1.2rem !important;
        }}
        .sc-title {{
            font-size: 1.45rem !important;
        }}
        .metric-val {{
            font-size: 1.3rem !important;
        }}
        .sticky-navbar {{
            flex-direction: column !important;
            gap: 10px !important;
            align-items: flex-start !important;
        }}
    }}

    /* Print Stylesheet for Invoices & Manifests */
    @media print {{
        header, [data-testid="stSidebar"], [data-testid="stToolbar"], .stButton, .no-print, .cookie-banner-box, .sticky-navbar, .site-footer {{
            display: none !important;
        }}
        .stApp {{
            background: #FFFFFF !important;
            color: #000000 !important;
        }}
        .printable-invoice {{
            display: block !important;
            border: 2px solid #000000 !important;
            padding: 25px !important;
            background: #FFFFFF !important;
            color: #000000 !important;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. INTERACTIVE CONFIRMATION MODALS & SUPPORT DIALOGS (@st.dialog)
# -------------------------------------------------------------
@st.dialog("🛒 Review & Confirm Order Dispatch")
def confirm_order_dialog(totals, dest_city, cart_items_data):
    st.markdown(f"#### 💳 Total Payable: **₹{totals['total']:,.2f}**")
    st.write(f"📍 **Destination Freight Hub**: {dest_city}")
    st.write(f"📦 **Cart Volume**: {len(cart_items_data)} unique SKUs ({sum(i['quantity'] for i in cart_items_data)} items)")
    
    st.markdown("---")
    st.caption("Are you sure you want to authorize this transaction and dispatch the consignment via the shortest Dijkstra path?")
    
    c_yes, c_no = st.columns(2)
    with c_yes:
        if st.button("✅ Yes, Confirm & Dispatch", type="primary", use_container_width=True):
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
            billing.export_order_to_csv(order_id, st.session_state.customer.username, dest_city, cart_items_data, totals)
            billing.send_invoice_email(st.session_state.customer.email, order_id, receipt_text)
            
            st.session_state.last_order_id = order_id
            st.session_state.last_receipt_text = receipt_text
            st.session_state.cart.clear()
            st.toast(f"Order #{order_id} Confirmed & Queued!", icon="🎉")
            st.rerun()

    with c_no:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


@st.dialog("⚠️ Confirm SKU Deletion")
def confirm_delete_sku_dialog(prod_id, prod_name):
    st.markdown(f"#### 🗑️ Delete Product #{prod_id}?")
    st.write(f"Are you sure you want to remove **{prod_name}** from the SQLite warehouse inventory?")
    st.caption("⚠️ This action is irreversible and immediately updates the active catalog.")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Permanently Delete", type="primary", use_container_width=True):
            database.delete_product(prod_id)
            st.toast(f"SKU #{prod_id} deleted!", icon="🗑️")
            st.rerun()
    with c2:
        if st.button("Abort", use_container_width=True):
            st.rerun()


@st.dialog("🎧 24/7 SmartCart Support Desk")
def support_desk_dialog():
    st.markdown("#### Autonomous Logistics & Retail Helpdesk")
    st.caption("Get instant assistance with routing delays, payments, or account permissions.")
    
    user_label = st.session_state.auth_user["username"] if st.session_state.auth_user else "Guest Visitor"
    st.text_input("Requester Identity", value=user_label, disabled=True)
    t_cat = st.selectbox("Inquiry Department", [
        "🚚 Dijkstra Delivery Routing / Dispatch Tracking",
        "💳 Billing, GST Invoicing & Tax Receipts",
        "🏪 Merchant / Seller Catalog Onboarding",
        "🔌 TCP Socket POS & Terminal Connectivity",
        "🔒 Account & Authentication Security"
    ])
    t_msg = st.text_area("Issue Description", placeholder="Describe your question or operational issue in detail...")
    
    if st.button("Submit Support Ticket", type="primary", use_container_width=True):
        if t_msg.strip():
            ticket_id = f"SC-TKT-{abs(hash(t_msg)) % 90000 + 10000}"
            st.success(f"Ticket #{ticket_id} opened successfully! A logistics engineer has been notified.")
        else:
            st.error("Please enter issue details before submitting.")


# -------------------------------------------------------------
# 4. ACCESSIBILITY SKIP-LINK & SCROLL PROGRESS SCRIPT
# -------------------------------------------------------------
st.markdown('<a href="#main-store-content" class="skip-to-content">Skip to Main Content ➔</a>', unsafe_allow_html=True)
st.markdown('<div id="scroll-progress-line"></div>', unsafe_allow_html=True)

# Attach Scroll Progress listener via parent document
st.components.v1.html("""
    <script>
    const updateProgress = () => {
        try {
            const doc = window.parent.document.documentElement;
            const scrollTotal = doc.scrollHeight - doc.clientHeight;
            if (scrollTotal > 0) {
                const scrollPct = (window.parent.scrollY / scrollTotal) * 100;
                const bar = window.parent.document.getElementById('scroll-progress-line');
                if (bar) bar.style.width = scrollPct + '%';
            }
        } catch(e) {}
    };
    window.parent.document.addEventListener('scroll', updateProgress, { passive: true });
    </script>
""", height=0)

# -------------------------------------------------------------
# 5. STICKY TOP HEADER NAVBAR WITH BRANDING, SEARCH & THEME TOGGLE
# -------------------------------------------------------------
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([3, 4, 1.5, 1.5])

with nav_col1:
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; margin-top:5px;">
            <span style="font-size:1.6rem;">🛒</span>
            <div>
                <span style="font-weight:800; font-size:1.15rem; color:{text_primary}; letter-spacing:-0.02em;">SmartCart</span>
                <span style="font-size:0.75rem; color:{text_secondary}; font-family:'JetBrains Mono'; margin-left:6px;">v2.8</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with nav_col2:
    global_q = st.text_input(
        "Global Site Search",
        value=st.session_state.global_search,
        placeholder="🔍 Search catalog products, categories, SKU IDs...",
        label_visibility="collapsed",
        key="top_search_bar"
    )
    if global_q != st.session_state.global_search:
        st.session_state.global_search = global_q

with nav_col3:
    theme_label = "☀️ Light" if is_dark else "🌙 Dark"
    if st.button(f"🌓 {theme_label}", use_container_width=True, help="Toggle between Dark and Light mode"):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()

with nav_col4:
    if st.button("🎧 Support", use_container_width=True, help="Open 24/7 SmartCart Support Desk"):
        support_desk_dialog()

st.markdown('<div id="main-store-content"></div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. SIDEBAR NAVIGATION & AUTHENTICATION
# -------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sc-tag">SMARTCART FLEET OS // v2.8</div>', unsafe_allow_html=True)
    st.markdown("## **SmartCart** Logistics")
    st.caption("Central Operations & Commerce Hub")
    st.divider()

    # User Profile / Login Card
    if st.session_state.auth_user is None:
        st.markdown("#### 🔐 Access Gateway")
        auth_mode = st.radio("Mode", ["Sign In", "Register"], horizontal=True, label_visibility="collapsed")

        if auth_mode == "Sign In":
            l_user = st.text_input("Username", key="l_user", placeholder="Enter username")
            
            # Password visibility toggle
            col_lp1, col_lp2 = st.columns([3, 1.2])
            with col_lp2:
                show_l_pass = st.checkbox("👁️ Show", key="show_l_pass")
            with col_lp1:
                l_pass = st.text_input("Password", type="text" if show_l_pass else "password", key="l_pass", placeholder="••••••••")

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
                    st.toast(f"Welcome back, {user_row['username']}!", icon="👋")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

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
            st.markdown("#### 📝 Register Account")
            reg_role = st.radio(
                "Account Role",
                ["🛍️ Buyer (Customer)", "🏪 Seller (Merchant / Admin)"],
                horizontal=True,
                key="r_role"
            )
            is_seller_reg = "Seller" in reg_role

            reg_u = st.text_input("Username", key="r_u", placeholder="e.g. aryan_store or rahul")
            reg_e = st.text_input("Email", key="r_e", placeholder="e.g. name@example.com")
            
            # Password visibility toggle for registration
            col_rp1, col_rp2 = st.columns([3, 1.2])
            with col_rp2:
                show_r_pass = st.checkbox("👁️ Show", key="show_r_pass")
            with col_rp1:
                reg_p = st.text_input("Password", type="text" if show_r_pass else "password", key="r_p", placeholder="••••••••")

            cities = st.session_state.optimizer.get_all_cities()
            reg_c = st.selectbox("Operating Hub / Base City", cities, key="r_c")

            if is_seller_reg:
                st.info("🏪 **Seller Account**: Grants access to Warehouse Stock Control, Product Catalog Management, Sales Analytics, and System Telemetry.")
                reg_prem = False
            else:
                reg_prem = st.checkbox("Sign as Premium Customer (10% Off)", value=True)

            if st.button("Create Account", type="primary", use_container_width=True):
                chosen_role = "admin" if is_seller_reg else "customer"
                ok, msg = database.register_user(reg_u, reg_e, reg_p, reg_c, 1 if reg_prem else 0, role=chosen_role)
                if ok:
                    st.success(f"{msg} You registered as **{reg_role}**! Switch to 'Sign In' above to log in.")
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
        st.write(f"📍 Hub Node: **{user_info.get('city', 'Bengaluru')}**")

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
    st.markdown(f"""
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
                <div class="metric-val">{distance:,.0f} <span style="font-size:1rem;color:{text_secondary};">km</span></div>
                <div class="metric-delta delta-green">Dijkstra Solved</div>
            </div>
        """, unsafe_allow_html=True)
    with t_col2:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">⏱️ Estimated Transit</div>
                <div class="metric-val">{est_days} <span style="font-size:1rem;color:{text_secondary};">days</span></div>
                <div class="metric-delta delta-blue">Highway Speed 65 km/h</div>
            </div>
        """, unsafe_allow_html=True)
    with t_col3:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">⛽ Diesel Consumption</div>
                <div class="metric-val">{fuel_burn:,.0f} <span style="font-size:1rem;color:{text_secondary};">L</span></div>
                <div class="metric-delta delta-green">Heavy Freight Average</div>
            </div>
        """, unsafe_allow_html=True)
    with t_col4:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">🌱 Carbon Footprint</div>
                <div class="metric-val">{co2_footprint:,.0f} <span style="font-size:1rem;color:{text_secondary};">kg</span></div>
                <div class="metric-delta delta-blue">BS-VI Standard Fleet</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Interactive 3D GPS Delivery Tracking Map
    st.markdown("#### 🛰️ Interactive 3D OpenStreetMap GPS Tracker")
    st.caption("Live 3D WebGL render with highway flight arcs, city hubs, and real-time interpolated GPS vehicle pin coordinates.")

    c_map_left, c_map_right = st.columns([3, 1])

    with c_map_right:
        st.markdown("##### 📍 Active Telemetry")
        st.write(f"**Origin**: {path[0] if path else 'N/A'}")
        st.write(f"**Destination**: {path[-1] if path else 'N/A'}")
        st.write(f"**Waypoints**: {' ➔ '.join(path)}")

        st.divider()
        st.markdown("##### 🚚 Dispatch Driver Progress")
        
        # Check role: Buyer sees live status indicator, Seller/Admin can simulate journey progress
        is_seller = st.session_state.auth_user and st.session_state.auth_user["role"] == "admin"
        if is_seller:
            progress_val = st.slider("Dispatch Progress Simulation (%)", 0, 100, 45, step=5)
        else:
            progress_val = 55
            st.progress(progress_val / 100.0)
            st.caption(f"Status: **In Transit ({progress_val}% Completed)** • Driver en route")

        cur_lat, cur_lon, cur_leg = optimizer.interpolate_delivery_gps(path, progress_val)
        
        st.markdown(f"""
            <div class="feed-item">
                <div class="feed-title">📡 Current GPS Coordinates</div>
                <div class="feed-desc" style="font-family:'JetBrains Mono'; font-weight:700; color:{accent_blue};">
                    Lat: {cur_lat:.4f}° N<br/>Lon: {cur_lon:.4f}° E
                </div>
                <div class="feed-desc" style="margin-top:0.3rem;">Current Leg: <strong>{cur_leg}</strong></div>
            </div>
        """, unsafe_allow_html=True)

    with c_map_left:
        deck_chart = optimizer.create_interactive_deck(path, progress_percent=progress_val)
        st.pydeck_chart(deck_chart, use_container_width=True)

    st.divider()

    # Network Topology & Live Dispatch Feed
    col_topo, col_feed = st.columns([1.8, 1.2], gap="large")

    with col_topo:
        st.markdown("#### 🌐 Static Network Topology Graph")
        st.caption("NetworkX graph visualization with spring layout highlighting the active shortest path corridor.")
        fig_net = optimizer.visualize_network(path)
        st.pyplot(fig_net, use_container_width=True)

    with col_feed:
        st.markdown("#### ⚡ Live Logistics Dispatch Feed")
        feed_events = [
            ("FL-1092 DISPATCHED", "Truck departed Bengaluru Central Fulfillment toward Hyderabad.", "3 mins ago", "pill-green"),
            ("TOLL GATE SYNC", "Automated FASTag debit at Devanahalli Plaza #4.", "14 mins ago", "pill-blue"),
            ("WEIGHT CHECK OK", "Axle load verified 18.4 MT at Electronic City Weighbridge.", "42 mins ago", "pill-green"),
            ("ROUTE OPTIMIZED", "SciPy Dijkstra bypassed NH-48 bottleneck via Outer Ring.", "1 hr ago", "pill-amber"),
            ("CARGO SCAN COMPLETE", "128 consignments RFID verified into container #SC-998.", "2 hrs ago", "pill-blue")
        ]
        for title, desc, t_ago, pill_cls in feed_events:
            st.markdown(f"""
                <div class="feed-item">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="feed-title">{title}</span>
                        <span class="pill {pill_cls}">{t_ago}</span>
                    </div>
                    <div class="feed-desc">{desc}</div>
                </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 2: STOREFRONT CATALOG & CART CHECKOUT
# -------------------------------------------------------------
elif menu == "🛍️ Catalog & Cart Checkout":
    st.markdown(f"""
        <div class="sc-hero">
            <div class="sc-tag">ECOMMERCE DISPATCH // INSTANT INVOICING</div>
            <h1 class="sc-title">Storefront Catalog & Fulfillment Cart</h1>
            <div class="sc-subtitle">Browse warehouse inventory, apply membership tier discounts, and generate official GST invoices.</div>
        </div>
    """, unsafe_allow_html=True)

    col_catalog, col_cart = st.columns([1.6, 1.4], gap="large")

    with col_catalog:
        st.markdown("#### 📦 Product Catalog")
        
        # Filtering & Search
        cf1, cf2 = st.columns([1, 1])
        with cf1:
            all_cats = ["All Categories"] + database.get_product_categories()
            chosen_cat = st.selectbox("Category", all_cats, label_visibility="collapsed")
        with cf2:
            sort_choice = st.selectbox("Sort By", ["Price: Low to High", "Price: High to Low", "Name: A-Z"], label_visibility="collapsed")

        # Combine local search with global header search
        active_search = st.session_state.global_search.strip()
        if active_search:
            st.caption(f"Showing results filtered by global search: **'{active_search}'**")

        products_list = database.get_all_products(category=chosen_cat if chosen_cat != "All Categories" else None)

        if active_search:
            products_list = [
                p for p in products_list 
                if active_search.lower() in p["name"].lower() or active_search.lower() in p["category"].lower()
            ]

        if sort_choice == "Price: Low to High":
            products_list.sort(key=lambda x: x["price"])
        elif sort_choice == "Price: High to Low":
            products_list.sort(key=lambda x: x["price"], reverse=True)
        elif sort_choice == "Name: A-Z":
            products_list.sort(key=lambda x: x["name"])

        if not products_list:
            st.info("No products match your search query. Try clearing the search bar.")

        for p in products_list:
            stock_pill = f'<span class="pill pill-green">✓ IN STOCK ({p["stock"]})</span>' if p['stock'] > 5 else (f'<span class="pill pill-amber">⚠️ LOW STOCK ({p["stock"]})</span>' if p['stock'] > 0 else '<span class="pill pill-red">✕ OUT OF STOCK</span>')

            st.markdown(f"""
                <div class="store-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="pill pill-blue">{p['category']}</span>
                        {stock_pill}
                    </div>
                    <div style="font-size:1.15rem; font-weight:700; color:{text_primary}; margin:0.4rem 0 0.2rem 0;">{p['name']}</div>
                    <div class="price-display">₹{p['price']:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)

            c_qty, c_btn = st.columns([1, 2])
            with c_qty:
                qty = st.number_input("Qty", min_value=1, max_value=max(1, p['stock']), value=1, key=f"q_{p['product_id']}", label_visibility="collapsed")
            with c_btn:
                if st.button("🛒 Add to Order", key=f"b_{p['product_id']}", use_container_width=True, disabled=(p['stock'] <= 0)):
                    if st.session_state.customer is None:
                        st.error("Please sign in as a Customer from the sidebar to purchase.")
                    else:
                        prod_obj = Product(p['product_id'], p['name'], p['category'], p['price'], p['stock'])
                        st.session_state.cart.add_item(prod_obj, qty)
                        st.toast(f"Added {qty}x {p['name']} to order!", icon="📦")
            st.write("")

    with col_cart:
        st.markdown("#### 🛒 Active Dispatch Order")

        if st.session_state.cart is None:
            st.markdown(f"""
                <div class="sc-card" style="text-align:center; padding:2.5rem 1rem;">
                    <div style="font-size:2.5rem; margin-bottom:0.5rem;">🔐</div>
                    <div style="font-weight:700; color:{text_primary};">Authentication Required</div>
                    <p style="color:{text_secondary}; font-size:0.85rem;">Sign in as a customer from the left sidebar to start building your cart.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            cart = st.session_state.cart
            if len(cart) == 0:
                st.markdown(f"""
                    <div class="sc-card" style="text-align:center; padding:2rem 1rem;">
                        <div style="font-size:2rem; margin-bottom:0.3rem;">🛒</div>
                        <div style="font-weight:700; color:{text_primary};">Your cart is empty</div>
                        <p style="color:{text_secondary}; font-size:0.85rem;">Select items from the catalog to prepare your bill.</p>
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
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem; color:{text_secondary};">
                            <span>Subtotal:</span><span>₹{totals['subtotal']:,.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem; color:#10B981;">
                            <span>Customer Discount ({disc_rate}%):</span><span>-₹{totals['discount_amount']:,.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem; color:{text_secondary};">
                            <span>GST Tax (5%):</span><span>₹{totals['tax']:,.2f}</span>
                        </div>
                        <hr style="border-color:{border_card}; margin:0.5rem 0;" />
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:700; color:{text_primary};">Total Payable:</span>
                            <span style="font-size:1.45rem; font-weight:800; color:{accent_blue}; font-family:'JetBrains Mono';">₹{totals['total']:,.2f}</span>
                        </div>
                        <div style="font-size:0.75rem; color:{text_secondary}; text-align:right; margin-top:0.2rem;">
                            Banker's rounded cash integer: ₹{totals['integer_rupees']:,}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                cities = st.session_state.optimizer.get_all_cities()
                dest_city = st.selectbox("Destination Hub", cities, index=cities.index(st.session_state.customer.city) if st.session_state.customer.city in cities else 0)

                # Promo coupon copy helper
                st.markdown("""
                    <div style="display:flex; align-items:center; justify-content:space-between; font-size:0.8rem; margin-bottom:0.6rem;">
                        <span>🎟️ Active Promo: <code>SMART10</code> (10% Off)</span>
                    </div>
                """, unsafe_allow_html=True)

                cart_items_data = [
                    {"product_id": item.product.product_id, "name": item.product.name, "quantity": item.quantity, "unit_price": item.product.price, "total_price": item.total_price}
                    for item in cart.iter_items()
                ]

                b1, b2 = st.columns([2, 1])
                with b1:
                    # Triggers confirmation modal before processing
                    if st.button("💳 Review & Dispatch Order", type="primary", use_container_width=True):
                        confirm_order_dialog(totals, dest_city, cart_items_data)

                with b2:
                    if st.button("Clear Order", use_container_width=True):
                        st.session_state.cart.clear()
                        st.rerun()

        # Display Last Confirmed Invoice & Print Option
        if "last_order_id" in st.session_state and st.session_state.last_order_id:
            st.divider()
            st.markdown(f"#### 📄 Order #{st.session_state.last_order_id} Documentation")
            st.balloons()
            
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                # Native print dialog trigger
                if st.button("🖨️ Print / Save PDF Invoice", use_container_width=True):
                    st.components.v1.html("<script>window.parent.print();</script>", height=0)
            with p_col2:
                csv_path = f"invoices/invoice_{st.session_state.last_order_id}.csv"
                if os.path.exists(csv_path):
                    with open(csv_path, "r") as f:
                        st.download_button(
                            label="📥 Download CSV Tax Invoice",
                            data=f.read(),
                            file_name=f"smartcart_invoice_{st.session_state.last_order_id}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )

            with st.expander("📄 View Formatted ASCII Receipt", expanded=True):
                st.code(st.session_state.last_receipt_text, language="text")

    # -------------------------------------------------------------
    # STOREFRONT EXPANDABLE FAQ ACCORDION
    # -------------------------------------------------------------
    st.divider()
    st.markdown("#### ❓ Frequently Asked Questions (FAQ) & System Policies")
    
    with st.expander("1. How does the Dijkstra Shortest-Path Logistics Engine operate?"):
        st.write("""
            SmartCart models India's national highway grid as a **NetworkX graph** with 21 transit nodes.
            When you select a destination city, **SciPy's sparse Compressed Sparse Row (CSR) Dijkstra algorithm** computes
            the mathematically shortest path, minimizing fuel consumption and transit delays.
        """)
    
    with st.expander("2. What are the key differences between Buyer and Seller accounts?"):
        st.write("""
            - **🛍️ Buyer (Customer)**: Can browse the real-time catalog, configure delivery destinations, claim membership discounts, checkout, and track GPS telemetry.
            - **🏪 Seller (Merchant / Admin)**: Has access to the **Warehouse Inventory Hub** to introduce new SKUs, modify retail pricing, restock units, audit transactions, and review revenue BI analytics.
        """)
        
    with st.expander("3. How does the Banker's Rounding and GST calculation work?"):
        st.write("""
            All product totals apply standard **5% GST** followed by Python's IEEE 754 Banker's rounding (`round()`),
            rounding half-values to the nearest even number. An integer truncated rupee representation (`math.trunc()`)
            is also supplied for cash POS cashiers.
        """)

    with st.expander("4. How do POS Terminals connect over TCP sockets?"):
        st.write("""
            Local cashier hardware communicates via `network_pos.py` using Python's standard `socket` module
            over IPv4 (`AF_INET`) stream sockets (`SOCK_STREAM`) on port `65432`.
        """)

# -------------------------------------------------------------
# TAB 3: BUSINESS INTELLIGENCE & REVENUE ANALYTICS
# -------------------------------------------------------------
elif menu == "📊 Business Intelligence & KPIs":
    st.markdown(f"""
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
                <div class="metric-val">{metrics['order_count']} <span style="font-size:0.9rem;color:{text_secondary};">orders</span></div>
                <div class="metric-delta delta-blue">ACID Logged in SQLite</div>
            </div>
        """, unsafe_allow_html=True)

    # UTM Marketing Attribution Card
    st.write("")
    utm = st.session_state.utm_params
    st.markdown(f"""
        <div class="feed-item" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div>
                <strong>📈 Campaign Attribution Telemetry (UTM)</strong><br/>
                <span style="font-size:0.82rem; color:{text_secondary};">
                    Source: <code>{utm['source']}</code> • Medium: <code>{utm['medium']}</code> • Campaign: <code>{utm['campaign']}</code>
                </span>
            </div>
            <div>
                <span class="pill pill-blue">UTM ENGINE ACTIVE</span>
            </div>
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
# TAB 4: WAREHOUSE INVENTORY HUB (ADMIN / SELLER)
# -------------------------------------------------------------
elif menu == "🛠️ Warehouse Inventory Hub":
    st.markdown(f"""
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

        if prod_dict:
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
                    st.toast(f"SKU #{selected_p['product_id']} updated!", icon="✅")
                    st.rerun()

            st.divider()
            # Triggers confirmation modal before deleting SKU
            if st.button("🗑️ Delete SKU from Catalog"):
                confirm_delete_sku_dialog(selected_p["product_id"], selected_p["name"])
        else:
            st.info("No products available to adjust.")

# -------------------------------------------------------------
# TAB 5: CLOUD ARCHIVAL & SYSTEM SERVICES
# -------------------------------------------------------------
elif menu == "⚙️ Cloud Archival & Services":
    st.markdown(f"""
        <div class="sc-hero">
            <div class="sc-tag">CONCURRENCY & NETWORKING // THREADING + FTP + SOCKETS</div>
            <h1 class="sc-title">Cloud Infrastructure & POS Network Gateway</h1>
            <div class="sc-subtitle">Background daemon threads, automated FTP archival, and low-level TCP socket listeners.</div>
        </div>
    """, unsafe_allow_html=True)

    b1, b2 = st.columns(2, gap="large")
    with b1:
        st.markdown("#### ☁️ Asynchronous Database Archival")
        st.write("Spawns a background worker thread (`threading.Thread`) that transmits an encrypted database snapshot over FTP (`ftplib`) without stalling UI telemetry.")
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

# -------------------------------------------------------------
# 7. DISMISSIBLE PRIVACY COOKIE CONSENT BANNER
# -------------------------------------------------------------
if not st.session_state.cookies_accepted:
    st.markdown(f"""
        <div class="cookie-banner-box">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                <div>
                    <strong>🍪 SmartCart Privacy & Cookie Preferences</strong><br/>
                    <span style="font-size:0.83rem; color:{text_secondary};">
                        We use essential session tokens to persist your cart, active Dijkstra routing telemetry, and authentication state.
                    </span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    c_ck1, c_ck2, _ = st.columns([1.5, 1.5, 5])
    with c_ck1:
        if st.button("Accept All Cookies", key="cookie_accept_btn", type="primary", use_container_width=True):
            st.session_state.cookies_accepted = True
            st.rerun()
    with c_ck2:
        if st.button("Essential Only", key="cookie_decline_btn", use_container_width=True):
            st.session_state.cookies_accepted = True
            st.rerun()

# -------------------------------------------------------------
# 8. DYNAMIC LAST UPDATED FOOTER & BACK-TO-TOP BUTTON
# -------------------------------------------------------------
last_sync_timestamp = datetime.now().strftime("%B %d, %Y • %H:%M:%S IST")

st.markdown(f"""
    <div class="site-footer">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
            <div>
                <strong>SmartCart Logistics Engine</strong> // Academic & Production Release v2.8.0<br/>
                <span style="font-size:0.75rem; color:{text_secondary};">Python Syllabus: OOP • SQLite • NumPy • SciPy • NetworkX • Threading • Sockets • FTP</span>
            </div>
            <div>
                <span class="status-pulse">●</span> All Services Operational • Database: SQLite (ACID)
            </div>
            <div>
                🕒 Last Synchronized: <strong>{last_sync_timestamp}</strong>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Floating Back-to-Top Button
f_col1, f_col2 = st.columns([6, 1])
with f_col2:
    st.markdown("""
        <div style="text-align:right; margin-top:0.5rem;">
            <a href="#top" style="text-decoration:none;">
                <span class="pill pill-blue" style="cursor:pointer; padding:6px 14px;">🔝 Back to Top</span>
            </a>
        </div>
    """, unsafe_allow_html=True)
