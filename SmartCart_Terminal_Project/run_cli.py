"""
run_cli.py
Terminal-based Command Line Interface for Online Shopping & Billing System
Allows full interactive testing in the console without opening a browser.
Demonstrates:
  - Sessions 1-6: Control flow, loops, string formatting, list operations
  - Sessions 7-10: OOP, SQLite, Invoicing, Routing, Analytics, Threading
  - User Authentication: Secure Password Verification & Role-Based Access
"""

import sys
import os
import database
from models import Product, Customer, Admin, ShoppingCart
import billing
import routing
import analytics
import backup_service
import threading


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def print_banner():
    print("=" * 60)
    print("      SMARTCART - ONLINE SHOPPING & BILLING SYSTEM          ")
    print("        Integrated Logistics & Analytics Engine             ")
    print("=" * 60)


def login_prompt():
    """Initial authentication prompt in terminal."""
    while True:
        print_banner()
        print("1. Log In to Existing Account")
        print("2. Register New Customer Account")
        print("3. Quick Demo Login as Customer (Rahul Sharma)")
        print("4. Quick Demo Login as Store Admin (Admin User)")
        print("5. Academic Viva Voce Defense Console (Sessions 1-10)")
        print("6. Exit")
        print("-" * 60)

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            u_name = input("Username: ").strip()
            u_pass = input("Password: ").strip()
            user_row = database.authenticate_user(u_name, u_pass)
            if user_row:
                print(f"\n[OK] Login successful. Welcome, {user_row['username']}.")
                return user_row
            else:
                print("\n[ERROR] Invalid username or password.")
                input("Press Enter to try again...")

        elif choice == "2":
            print("\n--- NEW USER REGISTRATION ---")
            role_sel = input("Select Account Type:\n  1. Buyer (Customer)\n  2. Seller (Merchant / Admin)\nChoice (default 1): ").strip()
            role = "admin" if role_sel == "2" else "customer"
            u_name = input("Choose Username: ").strip()
            u_email = input("Enter Email: ").strip()
            u_pass = input("Create Password: ").strip()
            u_city = input("City (e.g. Mumbai, Delhi, Bengaluru): ").strip()
            prem = False
            if role == "customer":
                prem = input("Apply for Premium Discount 10%? (y/n): ").strip().lower() == "y"
            ok, msg = database.register_user(u_name, u_email, u_pass, u_city, 1 if prem else 0, role=role)
            print(f"\n{'[OK]' if ok else '[ERROR]'} {msg}")
            if ok:
                print(f"Registered as: {'Seller (Admin)' if role == 'admin' else 'Buyer (Customer)'}")
            input("Press Enter to continue...")

        elif choice == "3":
            return database.authenticate_user("rahul_sharma", "pass123")

        elif choice == "4":
            return database.authenticate_user("admin_user", "admin123")

        elif choice == "5":
            show_viva_defense_cli()

        elif choice == "6":
            sys.exit(0)


def cli_storefront():
    optimizer = routing.LogisticsOptimizer()
    user_row = login_prompt()

    is_admin = user_row["role"] == "admin"

    if not is_admin:
        customer = Customer(
            user_id=user_row["user_id"],
            username=user_row["username"],
            email=user_row["email"],
            city=user_row["city"],
            is_premium=bool(user_row["is_premium"])
        )
        cart = ShoppingCart(customer)
    else:
        customer = None
        cart = None

    while True:
        print_banner()
        if is_admin:
            print(f"Logged in as: [ADMIN] {user_row['username']} | Role: System Administrator")
            print("-" * 60)
            print("1. Browse Catalog")
            print("2. Add New Product to Inventory")
            print("3. Restock / Update Product Price")
            print("4. Delete Product from Catalog")
            print("5. View Delivery Road Network")
            print("6. Business Intelligence & Revenue Dashboard")
            print("7. Run Database Cloud Backup")
            print("8. Log Out / Switch User")
        else:
            print(f"Logged in as: {customer.username} | Status: {'Premium (10% Off)' if customer.is_premium else 'Regular'} | Cart Items: {len(cart)}")
            print("-" * 60)
            print("1. Browse Catalog & Add to Cart")
            print("2. View Cart & Modify Items")
            print("3. Checkout & Generate Bill")
            print("4. Delivery Route Optimizer")
            print("5. Log Out / Switch User")
        print("-" * 60)

        choice = input("Enter your selection: ").strip()

        # CUSTOMER FLOW
        if not is_admin:
            if choice == "1":
                print("\n--- AVAILABLE PRODUCTS ---")
                products = database.get_all_products()
                for p in products:
                    print(f"ID: {p['product_id']:<3} | {p['name']:<35} | ₹{p['price']:>8.2f} | Stock: {p['stock']}")
                
                try:
                    pid = int(input("\nEnter Product ID to purchase (or 0 to cancel): ").strip())
                    if pid == 0:
                        continue
                    qty = int(input("Enter Quantity: ").strip())
                    p_row = database.get_product(pid)
                    if not p_row:
                        print("[ERROR] Product not found.")
                    elif qty > p_row["stock"]:
                        print(f"[ERROR] Insufficient stock. Only {p_row['stock']} available.")
                    else:
                        prod_obj = Product(p_row["product_id"], p_row["name"], p_row["category"], p_row["price"], p_row["stock"])
                        cart.add_item(prod_obj, qty)
                        print(f"[OK] Added {qty}x '{p_row['name']}' to your cart.")
                except ValueError:
                    print("[ERROR] Invalid input. Please enter valid numeric values.")
                input("\nPress Enter to continue...")

            elif choice == "2":
                print("\n--- YOUR SHOPPING CART ---")
                if len(cart) == 0:
                    print("Your cart is currently empty.")
                else:
                    for item in cart.iter_items():
                        print(f"- {item.product.name:<32} x {item.quantity:<3} = INR {item.total_price:.2f}")
                    totals = cart.calculate_totals()
                    print("-" * 50)
                    print(f"Subtotal: INR {totals['subtotal']:.2f}")
                    print(f"Discount: -INR {totals['discount_amount']:.2f}")
                    print(f"Tax (5%): INR {totals['tax']:.2f}")
                    print(f"Total:    INR {totals['total']:.2f} (Rounded: INR {totals['integer_rupees']})")
                input("\nPress Enter to continue...")

            elif choice == "3":
                if len(cart) == 0:
                    print("[ERROR] Cart is empty. Add products first before checkout.")
                    input("\nPress Enter to continue...")
                    continue

                print("\n--- CHECKOUT & BILLING ---")
                cities = optimizer.get_all_cities()
                print("Available Delivery Destinations:")
                for i, city in enumerate(cities, 1):
                    print(f"{i}. {city}")
                
                try:
                    city_idx = int(input("\nSelect destination city number: ").strip()) - 1
                    dest_city = cities[city_idx] if 0 <= city_idx < len(cities) else customer.city
                except (ValueError, IndexError):
                    dest_city = customer.city

                totals = cart.calculate_totals()
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

                # Save in SQLite
                order_id = database.save_order(
                    user_id=customer.user_id,
                    order_date="2026-10-01 11:00:00",
                    subtotal=totals["subtotal"],
                    discount=totals["discount_amount"],
                    tax=totals["tax"],
                    total=totals["total"],
                    delivery_city=dest_city,
                    items=cart_items_data
                )

                # Generate Text Receipt & CSV
                receipt_text = billing.generate_text_receipt(order_id, customer.username, dest_city, cart_items_data, totals)
                csv_path = billing.export_order_to_csv(order_id, customer.username, dest_city, cart_items_data, totals)

                print("\n" + receipt_text)
                print(f"\n[OK] Order #{order_id} recorded in database.")
                print(f"[OK] Text invoice saved to: invoices/invoice_{order_id}.txt")
                print(f"[OK] CSV spreadsheet saved to: {csv_path}")

                # Send Email
                billing.send_invoice_email(customer.email, order_id, receipt_text)

                cart.clear()
                input("\nPress Enter to continue...")

            elif choice == "4":
                print("\n--- DELIVERY ROUTE ---")
                cities = optimizer.get_all_cities()
                for i, city in enumerate(cities, 1):
                    print(f"{i}. {city}")
                try:
                    c_idx = int(input("\nSelect destination city to route from Bengaluru: ").strip()) - 1
                    target_city = cities[c_idx] if 0 <= c_idx < len(cities) else cities[0]
                except (ValueError, IndexError):
                    target_city = cities[0]

                path, distance = optimizer.find_shortest_route(target_city)
                print(f"\nOptimal Transit Path: {' -> '.join(path)}")
                print(f"Total Road Distance: {distance} km")

                fig = optimizer.generate_route_plot(path)
                chart_file = "route_map.png"
                fig.savefig(chart_file, dpi=150)
                print(f"Route map saved as '{chart_file}'.")
                input("\nPress Enter to continue...")

            elif choice == "5":
                return cli_storefront()

        # ADMIN FLOW
        else:
            if choice == "1":
                print("\n--- CURRENT STORE CATALOG ---")
                prods = database.get_all_products()
                for p in prods:
                    print(f"ID: {p['product_id']:<3} | {p['name']:<35} | ₹{p['price']:>8.2f} | Stock: {p['stock']} units")
                input("\nPress Enter to continue...")

            elif choice == "2":
                print("\n--- ADD NEW PRODUCT ---")
                name = input("Product Name: ").strip()
                cat = input("Category (Electronics/Fashion/etc): ").strip()
                try:
                    price = float(input("Unit Price (₹): ").strip())
                    stock = int(input("Initial Stock Quantity: ").strip())
                    new_id = database.add_product(name, cat, price, stock)
                    print(f"[OK] Product created successfully with ID #{new_id}.")
                except ValueError:
                    print("[ERROR] Invalid numeric inputs.")
                input("\nPress Enter to continue...")

            elif choice == "3":
                print("\n--- RESTOCK / UPDATE PRODUCT ---")
                try:
                    pid = int(input("Enter Product ID to update: ").strip())
                    new_price = float(input("Enter New Price (₹): ").strip())
                    new_stock = int(input("Enter New Stock: ").strip())
                    if database.update_product_details(pid, new_price, new_stock):
                        print(f"[OK] Product #{pid} updated successfully.")
                    else:
                        print("[ERROR] Product ID not found.")
                except ValueError:
                    print("[ERROR] Invalid input.")
                input("\nPress Enter to continue...")

            elif choice == "4":
                try:
                    pid = int(input("Enter Product ID to DELETE: ").strip())
                    if database.delete_product(pid):
                        print(f"[OK] Product #{pid} deleted from catalog.")
                    else:
                        print("[ERROR] Product ID not found.")
                except ValueError:
                    print("[ERROR] Invalid input.")
                input("\nPress Enter to continue...")

            elif choice == "5":
                path, distance = optimizer.find_shortest_route("Delhi")
                print(f"Sample Route to Delhi: {' -> '.join(path)} ({distance} km)")
                fig = optimizer.generate_route_plot(path)
                fig.savefig("route_map.png", dpi=150)
                print("Saved 'route_map.png'.")
                input("\nPress Enter to continue...")

            elif choice == "6":
                metrics = analytics.compute_sales_metrics()
                print(f"Total Revenue: ₹{metrics['total_revenue']:,.2f}")
                fig = analytics.generate_sales_dashboard()
                fig.savefig("sales_analytics.png", dpi=150)
                print("Saved 'sales_analytics.png'.")
                input("\nPress Enter to continue...")

            elif choice == "7":
                backup_service.run_async_backup()
                input("\nPress Enter to continue...")

            elif choice == "8":
                return cli_storefront()


def show_viva_defense_cli():
    """Interactive Viva Voce Defense Guide & Concepts Explorer in Terminal."""
    while True:
        print("\n" + "=" * 65)
        print("   SMARTCART VIVA VOCE & CURRICULUM DEFENSE CONSOLE   ")
        print("=" * 65)
        print("1. View Complete Sessions 1–10 Curriculum-to-Code Mapping")
        print("2. Test Banker's Rounding vs Round-Half-Up (Live Simulation)")
        print("3. Test TCP POS Socket Communication (network_pos.py)")
        print("4. Test Multithreaded Background FTP Archival (threading.Thread)")
        print("5. View Top 5 High-Yield Viva Questions & Answers")
        print("6. Return to Main Menu")
        print("-" * 65)
        sub = input("Enter choice (1-6): ").strip()

        if sub == "1":
            print("\n--- CURRICULUM TOPIC TO CODE MAPPING ---")
            topics = [
                ("Session 1", "Operators & Banker's Rounding", "models.py (calculate_totals)"),
                ("Session 2", "Loops & Control Flow (range)", "database.py, run_cli.py"),
                ("Session 3", "File I/O, datetime & CSV", "billing.py (export_order_to_csv)"),
                ("Session 4", "Lists, List Comprehension & Slicing", "models.py, app.py"),
                ("Session 5", "Sets, Dictionaries & Nested Dicts", "models.py, database.py"),
                ("Session 6", "String Alignment (ljust, rjust, center)", "billing.py (generate_text_receipt)"),
                ("Session 7", "Functions, lambda, map() & yield generator", "models.py (iter_items, subtotal)"),
                ("Session 8", "OOP (Encapsulation, Inheritance, Polymorphism)", "models.py (Product, User, Customer)"),
                ("Session 9", "SQLite3 WAL ACID & Sockets POS", "database.py, network_pos.py"),
                ("Session 10", "Multithreading, FTP, NumPy & SciPy Dijkstra", "backup_service.py, analytics.py, routing.py")
            ]
            for s, t, c in topics:
                print(f"[{s:<10}] {t:<42} -> {c}")
            input("\nPress Enter to continue...")

        elif sub == "2":
            print("\n--- BANKER'S ROUNDING (IEEE 754) SIMULATOR ---")
            try:
                val = float(input("Enter a floating point number (e.g. 2.5, 3.5, 12.55): ").strip())
                python_round = round(val)
                math_round = int(val + 0.5) if val > 0 else int(val - 0.5)
                print(f"\nValue Entered   : {val}")
                print(f"Python round()  : {python_round} (Nearest Even Integer - Eliminates penny bias)")
                print(f"Math Round-Up   : {math_round} (Always rounds away from zero - Produces drift)")
            except ValueError:
                print("[ERROR] Invalid number.")
            input("\nPress Enter to continue...")

        elif sub == "3":
            print("\n--- TESTING TCP SOCKET POS TERMINAL ---")
            import network_pos
            res = network_pos.send_pos_transaction({"terminal": "CLI_Examiner", "total": 9999.0, "items": 3})
            print(f"Socket Protocol : TCP/IP (AF_INET, SOCK_STREAM, Port {network_pos.DEFAULT_PORT})")
            print(f"Server Response : {res}")
            input("\nPress Enter to continue...")

        elif sub == "4":
            print("\n--- DISPATCHING MULTITHREADED BACKUP ---")
            worker = backup_service.run_async_backup()
            print(f"[OK] Dispatched Thread '{worker.name}' (daemon={worker.daemon})")
            print(f"Active Threads Count: {threading.active_count()}")
            input("\nPress Enter to continue...")

        elif sub == "5":
            print("\n--- TOP HIGH-YIELD VIVA QUESTIONS & DEFENSE ---")
            qa = [
                ("Q: What is Banker's Rounding and why use it?",
                 "A: Python's round() implements IEEE 754 round-half-to-even. It rounds .5 to the nearest even number (2.5 -> 2, 3.5 -> 4), eliminating cumulative penny drift in high-volume transactions."),
                ("Q: How does Dijkstra work in routing.py?",
                 "A: We construct an undirected weighted graph of Indian corridors in NetworkX, export it to a SciPy Compressed Sparse Row (CSR) matrix, and execute scipy.sparse.csgraph.dijkstra in O(E + V log V)."),
                ("Q: How is Encapsulation enforced in models.py?",
                 "A: Product prices and stocks use double leading underscores (__price, __stock). Name-mangling protects them, while @property and @price.setter ensure validation (rejecting negative prices)."),
                ("Q: Why use Python generators (yield)?",
                 "A: ShoppingCart.iter_items() uses 'yield' to lazily stream items on-demand with O(1) extra memory instead of returning full list duplicates."),
                ("Q: Why configure SQLite with PRAGMA journal_mode=WAL?",
                 "A: Write-Ahead Logging allows readers not to block writers and writers not to block readers, enabling concurrency between the web GUI and CLI run_cli.py.")
            ]
            for q, a in qa:
                print(f"\n{q}\n{a}")
            input("\nPress Enter to continue...")

        elif sub == "6":
            break


if __name__ == "__main__":
    cli_storefront()
