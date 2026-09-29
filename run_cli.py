"""
run_cli.py
Terminal-based Command Line Interface for Online Shopping & Billing System
Allows full interactive testing in the console without opening a browser.
Demonstrates:
  - Sessions 1-6: Control flow, loops, string formatting, list operations
  - Sessions 7-10: OOP, SQLite, Invoicing, Routing, Analytics, Threading
"""

import sys
import os
import database
from models import Product, Customer, ShoppingCart
import billing
import routing
import analytics
import backup_service

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def print_banner():
    print("=" * 60)
    print("   🛒 SMARTCART - ONLINE SHOPPING & BILLING SYSTEM   ")
    print("     (Integrated Logistics & Analytics Engine)       ")
    print("=" * 60)


def cli_storefront():
    optimizer = routing.LogisticsOptimizer()
    customer = Customer(
        user_id=1,
        username="rahul_sharma",
        email="rahul.sharma@example.com",
        city="Mumbai",
        is_premium=True
    )
    cart = ShoppingCart(customer)

    while True:
        print_banner()
        print(f"Logged in as: {customer.username} | Status: {'★ Premium (10% Off)' if customer.is_premium else 'Regular'} | Cart Items: {len(cart)}")
        print("-" * 60)
        print("1. Browse Catalog & Add to Cart")
        print("2. View Cart & Modify Items")
        print("3. Checkout & Generate Bill (Automated Invoicing)")
        print("4. Delivery Route Optimizer (NetworkX + SciPy Dijkstra)")
        print("5. Admin Sales Analytics & Visual Dashboard (NumPy + Matplotlib)")
        print("6. Run Automated Database Cloud Backup (Threading + FTP)")
        print("7. Exit")
        print("-" * 60)

        choice = input("Enter your selection (1-7): ").strip()

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
                    print("❌ Product not found.")
                elif qty > p_row["stock"]:
                    print(f"❌ Insufficient stock! Only {p_row['stock']} available.")
                else:
                    prod_obj = Product(p_row["product_id"], p_row["name"], p_row["category"], p_row["price"], p_row["stock"])
                    cart.add_item(prod_obj, qty)
                    print(f"✅ Added {qty}x '{p_row['name']}' to your cart!")
            except ValueError:
                print("❌ Invalid input! Please enter valid numeric values.")
            input("\nPress Enter to continue...")

        elif choice == "2":
            print("\n--- YOUR SHOPPING CART ---")
            if len(cart) == 0:
                print("Your cart is currently empty.")
            else:
                for item in cart.iter_items():
                    print(f"• {item.product.name:<32} x {item.quantity:<3} = ₹{item.total_price:.2f}")
                totals = cart.calculate_totals()
                print("-" * 50)
                print(f"Subtotal: ₹{totals['subtotal']:.2f}")
                print(f"Discount: -₹{totals['discount_amount']:.2f}")
                print(f"Tax (5%): ₹{totals['tax']:.2f}")
                print(f"Total:    ₹{totals['total']:.2f} (Rounded: ₹{totals['integer_rupees']})")
            input("\nPress Enter to continue...")

        elif choice == "3":
            if len(cart) == 0:
                print("❌ Cart is empty! Add products first before checkout.")
                input("\nPress Enter to continue...")
                continue

            print("\n--- CHECKOUT & BILLING ---")
            cities = optimizer.get_all_cities()
            print("Available Delivery Destinations:")
            for i, city in enumerate(cities, 1):
                print(f"{i}. {city}")
            
            try:
                city_idx = int(input("\nSelect destination city number: ").strip()) - 1
                dest_city = cities[city_idx] if 0 <= city_idx < len(cities) else "Mumbai"
            except (ValueError, IndexError):
                dest_city = "Mumbai"

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
                order_date="2026-09-29 16:30:00",
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
            print(f"\n✅ Order #{order_id} recorded in SQLite database.")
            print(f"✅ Text invoice saved to: invoices/invoice_{order_id}.txt")
            print(f"✅ CSV spreadsheet saved to: {csv_path}")

            # Send Email (simulated or real SMTP)
            billing.send_invoice_email(customer.email, order_id, receipt_text)

            # Clear cart after successful checkout
            cart.clear()
            input("\nPress Enter to continue...")

        elif choice == "4":
            print("\n--- GRAPH-OPTIMIZED LOGISTICS ROUTE ---")
            cities = optimizer.get_all_cities()
            for i, city in enumerate(cities, 1):
                print(f"{i}. {city}")
            try:
                c_idx = int(input("\nSelect destination city to route from Bengaluru: ").strip()) - 1
                target_city = cities[c_idx] if 0 <= c_idx < len(cities) else cities[0]
            except (ValueError, IndexError):
                target_city = cities[0]

            path, distance = optimizer.find_shortest_route(target_city)
            print(f"\n🚚 Optimal Transit Path: {' ➔ '.join(path)}")
            print(f"📏 Total Road Distance: {distance} km (Computed via SciPy Dijkstra & NetworkX)")

            # Save visual map plot
            fig = optimizer.generate_route_plot(path)
            chart_file = "route_map.png"
            fig.savefig(chart_file, dpi=150)
            print(f"📊 Graph visualization saved as '{chart_file}'.")
            input("\nPress Enter to continue...")

        elif choice == "5":
            print("\n--- BUSINESS INTELLIGENCE & REVENUE ANALYTICS ---")
            metrics = analytics.compute_sales_metrics()
            print(f"Total Revenue Generated : ₹{metrics['total_revenue']:,.2f}")
            print(f"Average Order Value     : ₹{metrics['average_order_value']:,.2f}")
            print(f"Highest Order Value     : ₹{metrics['max_order_value']:,.2f}")
            print(f"Total Transactions Log  : {metrics['order_count']}")
            print(f"Revenue Variance (Std)  : ₹{metrics['revenue_std_dev']:,.2f}")

            fig = analytics.generate_sales_dashboard()
            chart_file = "sales_analytics.png"
            fig.savefig(chart_file, dpi=150)
            print(f"\n📊 Analytics dashboard chart saved as '{chart_file}'.")
            input("\nPress Enter to continue...")

        elif choice == "6":
            print("\n--- CLOUD BACKUP SERVICE (THREADING + FTP) ---")
            backup_service.run_async_backup()
            input("\nPress Enter to continue...")

        elif choice == "7":
            print("\nExiting SmartCart. Happy shopping!")
            break


if __name__ == "__main__":
    cli_storefront()
