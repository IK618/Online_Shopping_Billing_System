# billEX & SmartCart: Online Shopping, Invoicing & Multi-Tenant Retail POS System
> **An Integrated Retail Invoicing, Graph-Optimized Logistics & Multi-Tenant POS Platform**

Synthesizes **Core Python, OOP, Relational Databases, Scientific Computing, Graph Algorithms, and Concurrency**.

---

## Key Highlights & Features

1. **Multi-Tenant POS & Store Identity Architecture**
   * Multi-store registration with unique store profiles (Shop Name, Physical Address, GSTIN, Phone, City).
   * Role-Based Access Control (RBAC): Store Owner (Admin) vs. Cashier Staff (Employee).
   * Admin security gates protecting master inventory pricing, staff management, and telemetry.

2. **Interactive Storefront & Dynamic Cart**
   * Real-time stock decrement and reactive inventory countdown.
   * Quantity stepper controls with overstock limits.
   * Customer discount tiering and promo code engine.
   * Banker's rounding and tax calculation (`math.trunc`, `round()`).

3. **Automated Multi-Format Invoicing & Cashier Attribution**
   * ASCII-formatted and printable tax receipts dynamically stamped with store address and GSTIN.
   * Cashier accountability tracking (`Billed By: [Cashier Name]`).
   * Export to `.csv` spreadsheet files with timestamps.
   * Automated email dispatch using Python's `smtplib` (`EmailMessage` over TLS port 587).

4. **Graph-Optimized Logistics & Delivery Routing**
   * Modeled with `networkx.Graph` representing major distribution hubs and highway distance weights.
   * Shortest delivery path computation using `scipy.sparse.csgraph.dijkstra` on sparse adjacency matrices.
   * Inter-city delivery freight calculation (free counter pickup in store home city).

5. **Business Intelligence & Sales Analytics**
   * Real-time transaction metrics computed with **NumPy** arrays (sum, mean, standard deviation, max/min).
   * 2-panel visual analytics dashboard with **Matplotlib** (Category sales bar chart + Weekly revenue line plot).

6. **Concurrency, Sockets & Cloud Archival**
   * Asynchronous database backups using `threading.Thread` and `ftplib` to prevent UI freezing.
   * Client-Server Point-of-Sale (POS) cashier terminal communication using `socket` (`AF_INET`, `SOCK_STREAM`).

---

## Syllabus Topic-to-Code Mapping

| Session | Curriculum Topic | Where It Is Implemented in the Code |
| :--- | :--- | :--- |
| **Session 1** | Operators, `math.trunc()`, `round()` (Banker's rounding) | [`models.py`](models.py) (`calculate_totals`) |
| **Session 2** | `range()`, loops, control flow | [`database.py`](database.py), [`run_cli.py`](run_cli.py) |
| **Session 3** | `datetime`, `random`, File I/O (`with open`), `csv` | [`billing.py`](billing.py) (`export_order_to_csv`, `generate_text_receipt`) |
| **Session 4** | Lists, List comprehension, Slicing | [`app.py`](app.py), [`models.py`](models.py) |
| **Session 5** | Sets, Dictionaries, Nested Structures | [`models.py`](models.py), [`database.py`](database.py) |
| **Session 6** | Strings (`ljust`, `rjust`, `center`, `strip`, format codes) | [`billing.py`](billing.py) |
| **Session 7** | Functions, `lambda`, `map()`, generators (`yield`) | [`models.py`](models.py) (`ShoppingCart.iter_items`, `calculate_subtotal`) |
| **Session 8** | OOP (`class`, inheritance, encapsulation, polymorphism) | [`models.py`](models.py) (`User` -> `Customer`, `Admin`, `Product`) |
| **Session 9** | SQLite (`sqlite3` CRUD, transactions, joins) | [`database.py`](database.py) |
| **Session 9** | `smtplib` (Email, port 587, starttls, EmailMessage) | [`billing.py`](billing.py) |
| **Session 9** | Sockets (`socket`, `bind`, `listen`, `send`, `recv`) | [`network_pos.py`](network_pos.py) |
| **Session 10** | Multithreading (`threading.Thread`, `active_count`) | [`backup_service.py`](backup_service.py) |
| **Session 10** | FTP (`ftplib.FTP`, `connect`, `login`, `storbinary`) | [`backup_service.py`](backup_service.py) |
| **Session 10** | NumPy (`ndarray`, `mean`, `sum`, `std`, vectorization) | [`analytics.py`](analytics.py) |
| **Session 10** | SciPy (`scipy.sparse.csgraph.dijkstra`, Adjacency Matrix) | [`routing.py`](routing.py) |
| **Session 10** | Matplotlib (`bar`, `plot`, subplots, annotations) | [`analytics.py`](analytics.py), [`routing.py`](routing.py) |
| **Session 10** | NetworkX (`Graph`, `add_edge`, `draw_networkx`) | [`routing.py`](routing.py) |

---

## How to Run the Project

### 1. Run the billEX Multi-Tenant Web POS Server (Port 8080)
```bash
python fastspring_server.py
```
*Access the billEX web POS application at `http://localhost:8080`.*

### 2. Run the Interactive Terminal CLI (Console Mode)
```bash
python run_cli.py
```
*Or run the isolated standalone version in `SmartCart_Terminal_Project/`:*
```bash
cd SmartCart_Terminal_Project
python run_cli.py
```

### 3. Test the Network POS Socket Client-Server
```bash
python network_pos.py
```

---

## Project Structure

```text
Online_Shopping_Billing_System/
├── invoices/                    # Generated text and CSV invoices
├── models.py                    # OOP data models, inheritance, generator & math rules
├── database.py                  # Multi-tenant SQLite schema, shops, staff, queries
├── billing.py                   # Formatted ASCII receipts, CSV export, and SMTP sender
├── fastspring_server.py         # Multi-threaded billEX HTTP server & REST API (Port 8080)
├── fastspring_ui.html           # billEX React 18 frontend with SVG icons & non-blocking toasts
├── routing.py                   # NetworkX & SciPy Dijkstra road route optimization
├── analytics.py                 # NumPy business metrics & Matplotlib chart generator
├── network_pos.py               # Socket client-server POS communication
├── backup_service.py            # Background threading worker & FTP cloud archival
├── run_cli.py                   # Complete interactive Terminal CLI menu
├── SmartCart_Terminal_Project/  # Isolated, preserved original terminal CLI project
├── requirements.txt             # Pinned Python package dependencies
├── .gitignore                   # Excludes caches, venv, and temporary databases
└── README.md                    # Project documentation and evaluation guide
```
