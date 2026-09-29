# SmartCart: Online Shopping & Billing System
> **An Integrated Retail Invoicing, Graph-Optimized Logistics & Sales Analytics Platform**

Built as a comprehensive 2nd-Year Python Project synthesizing **Core Python, OOP, Relational Databases, Scientific Computing, Graph Algorithms, and Concurrency**.

---

## 🌟 Key Highlights & Features

1. **🛍️ Interactive Storefront & Dynamic Cart**
   * Real-time stock decrement and inventory control.
   * Customer discount tiering (Regular vs. Premium Customer).
   * Banker's rounding and tax calculation (`math.trunc`, `round()`).

2. **🧾 Automated Multi-Format Invoicing**
   * ASCII-formatted tax receipts formatted with string alignment methods (`ljust`, `rjust`, `center`).
   * Export to `.csv` spreadsheet files with timestamps.
   * Automated email dispatch using Python's `smtplib` (`EmailMessage` over TLS port 587).

3. **🚚 Graph-Optimized Logistics & Delivery Routing**
   * Modeled with `networkx.Graph` representing major distribution hubs and highway distance weights.
   * Shortest delivery path computation using **`scipy.sparse.csgraph.dijkstra`** on sparse adjacency matrices.
   * Visual map rendering with **`matplotlib.pyplot`** highlighting the chosen transit corridor.

4. **📊 Business Intelligence & Sales Analytics**
   * Real-time transaction metrics computed with **NumPy** arrays (sum, mean, standard deviation, max/min).
   * 2-panel visual analytics dashboard with **Matplotlib** (Category sales bar chart + Weekly revenue line plot).

5. **⚙️ Concurrency, Sockets & Cloud Archival**
   * Asynchronous database backups using **`threading.Thread`** and **`ftplib`** to prevent UI freezing.
   * Client-Server Point-of-Sale (POS) cashier terminal communication using **`socket`** (`AF_INET`, `SOCK_STREAM`).

---

## 🎓 Syllabus Topic-to-Code Mapping

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

## 🚀 How to Run the Project

### 1. Run the Modern Web UI (Streamlit)
```bash
source .venv/bin/activate
streamlit run app.py
```
*The app will automatically open in your web browser at `http://localhost:8501`.*

### 2. Run the Interactive Terminal CLI (Console Mode)
```bash
source .venv/bin/activate
python run_cli.py
```

### 3. Test the Network POS Socket Client-Server
```bash
source .venv/bin/activate
python network_pos.py
```

---

## 📁 Project Structure

```text
Online_Shopping_Billing_System/
├── .venv/                   # Python virtual environment (ignored in git/zip)
├── invoices/                # Generated text and CSV invoices
├── models.py                # OOP data models, inheritance, generator & math rules
├── database.py              # SQLite connection, schema, queries, and seeding
├── billing.py               # Formatted ASCII receipts, CSV export, and SMTP sender
├── routing.py               # NetworkX & SciPy Dijkstra road route optimization
├── analytics.py             # NumPy business metrics & Matplotlib chart generator
├── network_pos.py           # Socket client-server POS communication
├── backup_service.py        # Background threading worker & FTP cloud archival
├── run_cli.py               # Complete interactive Terminal CLI menu
├── app.py                   # Full Streamlit Web UI application
├── requirements.txt         # Pinned Python package dependencies
├── .gitignore               # Excludes caches, venv, and temporary databases
└── README.md                # Project documentation and evaluation guide
```

---

## 🎯 Viva / Exam Defense Cheatsheet

1. **Q: How does the delivery routing work?**
   * *A:* We model India's major shipping corridors as a weighted graph in `NetworkX`. To find the optimal route, we convert the graph into a SciPy Compressed Sparse Row (CSR) adjacency matrix and execute Dijkstra's algorithm via `scipy.sparse.csgraph.dijkstra` in $O(E + V \log V)$ time.

2. **Q: Where is Multithreading used?**
   * *A:* In `backup_service.py`, database uploads to the FTP server run on a detached daemon thread (`threading.Thread`). This prevents the application interface (UI or CLI) from blocking or freezing during heavy network transfers.

3. **Q: How is Encapsulation demonstrated in OOP?**
   * *A:* In `Product`, the attributes `__price` and `__stock` are private. Access and modification are mediated through getters and setter methods with input validation.

4. **Q: Where are Python Generators used?**
   * *A:* In `ShoppingCart.iter_items()`, we use the `yield` statement to stream cart items lazily without duplicating array memory.
