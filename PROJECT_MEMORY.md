# PROJECT MEMORY — billEX (formerly SmartCart / FastSpring UI)

## 1. Project Context & High-Level Objective
- **Repository**: `/home/ik7/Online_Shopping_Billing_System`
- **Standalone Terminal Version**: Preserved 100% intact in `/home/ik7/Online_Shopping_Billing_System/SmartCart_Terminal_Project/`.
- **Current Live Web Server**: Dedicated Python HTTP Server on port `8080` (`fastspring_server.py`) serving `fastspring_ui.html`.
- **Brand Evolution**: Moving from generic single-store demo to **billEX**: Multi-Tenant Merchant POS & Store Billing Suite.

---

## 2. Next Major Milestone: billEX Multi-Tenant & Role-Based Access Control (RBAC)
*User Instruction: Rebrand to **billEX**, allow merchants to register with their shop's identity and address, give them Admin access, and allow them to create Employee accounts with Cashier/Billing access.*

### Core Architectural Specifications for Tomorrow:
1. **Rebranding to billEX**:
   - Replace all "FastSpring" branding with modern **billEX** logos, typography, and badges.
   - Maintain the enterprise UI design tokens:
     - Primary Action Orange: `#FF772A` (Hover: `#E05E13`)
     - Link / Accent Blue: `#1479CE`
     - Dark Charcoal Neutral: `#16181A`
     - Backgrounds: `#FFFFFF` and `#F8FAFC`
     - Fonts: `Figtree` and `JetBrains Mono`

2. **Shop Identity & Onboarding**:
   - Store owners register their shop:
     - `shop_name` (e.g., "Apex Electronics & Retail")
     - `address` (e.g., "Shop #14, Brigade Road, Bengaluru - 560001")
     - `gstin` (e.g., "29ABCDE1234F1Z5")
     - `phone` (e.g., "+91 9876543210")
     - `city` (Delivery hub anchor)
   - Store Profile Settings tab in Admin to update shop details anytime.

3. **Role-Based Access Control (RBAC)**:
   - **Shop Owner / Store Admin**:
     - Full administrative control.
     - Add/update/delete inventory SKUs, manage stock and pricing.
     - Add/invite Employee accounts (Cashiers) with assigned staff names and usernames.
     - View Business Intelligence & Revenue Analytics (NumPy/SQLite vector telemetry).
     - Trigger background database archival backups.
   - **Employee / Cashier**:
     - Dedicated **Fast POS Billing Counter**.
     - Search & scan warehouse SKUs with real-time stock countdown.
     - Adjust quantities manually or via stepper `[-]` / `[+]`.
     - Enter customer name and contact.
     - Apply promo codes (e.g. `SMART10`) or store discounts.
     - Instant print/save official bill with shop branding.
     - **Locked**: Cannot alter master product pricing, cannot delete inventory, cannot modify store credentials.

4. **Branded Invoice Output**:
   - Every invoice header dynamically shows the **Shop's Name, Address, GSTIN, and Phone Number**.
   - Footer / metadata includes: `Billed by: Cashier [Employee Name]`.
   - CSV export and printable PDF receipts include these shop identity fields.

5. **Dijkstra Logistics Integration**:
   - Retained for store-to-customer inter-city delivery routes with fuel, carbon footprint, and shortest path freight calculation.

---

## 3. Current State & Recent Accomplishments
- **Cycle 5 Completed**: Purged 100% of emojis and non-standard unicode characters. Replaced with pure SVG vector icons (`Icons.ChevronDown`, `Icons.User`, `Icons.Trash2`, `Icons.ArrowRight`, `Icons.Check`, CSS stock status dots).
- **Cycle 6 Completed**: Real-time remaining stock countdown on catalog cards, overstock button locking, and cart quantity stepper controls `[-]`, `<input>`, `[+]`.
- **Cycle 7 Completed**:
  - Rebranded to **billEX** Enterprise Retail POS & Multi-Tenant Billing Suite.
  - Multi-tenant SQLite database architecture (`shops`, `users`, `products`, `orders`).
  - Shop onboarding modal and editable Store Identity (Address, GSTIN, Phone, City).
  - RBAC: Store Owner (Admin) vs Cashier Staff (Employee). Locked admin tabs with security warnings for cashiers.
  - Official tax invoices with store address/GSTIN headers and cashier attribution (`Billed By: [Cashier Name]`).
  - Modern non-blocking toast notifications replacing legacy `window.alert()`.
  - Zero terminal project features lost (preserved 100% in `SmartCart_Terminal_Project/`).
  - Verified via headless Chrome CDP with 8 high-resolution screenshots.

---

## 4. Suggested Innovations & Ideas for billEX (Cycle 8)
1. **Quick Barcode / SKU Scan**: Auto-focused barcode input where scanning an EAN/SKU and pressing Enter adds it immediately to the active bill.
2. **Tendered Cash & Change Calculator**: Input customer cash payment (e.g. ₹2,000 for ₹1,450 bill) and display change to return (₹550) on receipt.
3. **Dynamic UPI QR Code on Screen & Invoice**: Render standard NPCI QR code (`upi://pay?pa=shop@upi&pn=ApexRetail&am=1450.00`) directly on POS counter and invoice slip for instant phone payment.
4. **End-of-Day Cashier Register Z-Report**: Aggregate shift metrics by cashier (orders processed, total cash collected, UPI volume) before closing shift.
5. **WhatsApp / SMS Instant Digital Bill**: Provide a 1-click button to send bill summary or receipt link directly to customer's mobile number.

---

## 5. Key Files
- `fastspring_ui.html` (Frontend single-page app, React 18, clean SVG icons, billEX branding)
- `fastspring_server.py` (Multi-threaded HTTP backend with REST endpoints on port 8080)
- `database.py` (Multi-tenant SQLite schema, shop registration, staff management)
- `billing.py` (Dynamic billEX tax invoices and CSV export with shop branding)
- `store.db` (SQLite relational database)
- `progress.txt` (Iteration history)
- `SmartCart_Terminal_Project/` (Isolated standalone CLI version)
