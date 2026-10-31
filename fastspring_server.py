#!/usr/bin/env python3
"""
fastspring_server.py
Pixel-perfect FastSpring Digital Invoicing Web Application
Full-fidelity UI replica of https://fastspring.com/digital-invoicing/
Powered by Python SQLite, Dijkstra Shortest-Path Logistics, Invoicing & Analytics Backend.
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys

# Ensure local backend modules are accessible
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import database
import models
import billing
import routing
import analytics
import backup_service

PORT = 8080
optimizer = routing.LogisticsOptimizer()

class FastSpringHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(BASE_DIR, "fastspring_ui.html"), "rb") as f:
                self.wfile.write(f.read())
            return

        if path == "/api/products":
            prods = database.get_all_products()
            prod_list = [dict(p) for p in prods]
            self.send_json(prod_list)
            return

        if path == "/api/categories":
            cats = database.get_product_categories()
            self.send_json(cats)
            return

        if path == "/api/cities":
            cities = optimizer.get_all_cities()
            self.send_json(cities)
            return

        if path == "/api/metrics":
            m = analytics.compute_sales_metrics()
            self.send_json(m)
            return

        if path.startswith("/api/route"):
            query = urllib.parse.parse_qs(parsed.query)
            dest = query.get("dest", ["Delhi"])[0]
            route_path, distance = optimizer.find_shortest_route(dest)
            self.send_json({
                "dest": dest,
                "path": route_path,
                "distance": distance,
                "est_days": round(distance / 650.0, 1),
                "fuel_burn": round(distance * 0.32, 1),
                "co2_footprint": round(distance * 0.85, 1)
            })
            return

        if path == "/api/orders":
            orders = database.get_detailed_orders(limit=25)
            self.send_json([dict(o) for o in orders])
            return

        # Serve static files (assets, images)
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        data = json.loads(body) if body else {}

        if path == "/api/login":
            u_name = data.get("username", "")
            u_pass = data.get("password", "")
            user = database.authenticate_user(u_name, u_pass)
            if user:
                self.send_json({"success": True, "user": dict(user)})
            else:
                self.send_json({"success": False, "error": "Invalid username or password."}, status=401)
            return

        if path == "/api/register":
            u_name = data.get("username", "")
            u_pass = data.get("password", "")
            u_email = data.get("email", "")
            u_city = data.get("city", "Bengaluru")
            u_role = data.get("role", "customer")
            is_prem = bool(data.get("is_premium", False))
            success = database.register_user(u_name, u_pass, u_email, u_city, u_role, is_prem)
            if success:
                u = database.authenticate_user(u_name, u_pass)
                self.send_json({"success": True, "user": dict(u)})
            else:
                self.send_json({"success": False, "error": "Username already exists."}, status=400)
            return

        if path == "/api/checkout":
            user_id = data.get("user_id")
            items = data.get("items", [])  # list of {product_id, quantity}
            dest_city = data.get("dest_city", "Bengaluru")
            promo_code = data.get("promo_code", "").strip().upper()

            # Retrieve user
            user_row = database.get_connection().execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
            if not user_row:
                self.send_json({"success": False, "error": "User not found."}, status=404)
                return

            cust = models.Customer(user_row["user_id"], user_row["username"], user_row["email"], user_row["city"], bool(user_row["is_premium"]))
            cart = models.ShoppingCart(cust)

            for it in items:
                p_row = database.get_product(it["product_id"])
                if p_row and p_row["stock"] >= it["quantity"]:
                    p_obj = models.Product(p_row["product_id"], p_row["name"], p_row["category"], p_row["price"], p_row["stock"])
                    cart.add_item(p_obj, it["quantity"])

            totals = cart.calculate_totals()
            
            # Apply promo code SMART10
            if promo_code == "SMART10":
                promo_discount = round(totals["subtotal"] * 0.10, 2)
                totals["discount_amount"] = round(totals["discount_amount"] + promo_discount, 2)
                totals["total"] = max(0.0, round(totals["total"] - promo_discount, 2))
                totals["integer_rupees"] = int(totals["total"])

            # Compute route distance for delivery fee
            route_path, distance = optimizer.find_shortest_route(dest_city)
            delivery_fee = round(distance * 0.45, 2)
            totals["delivery_fee"] = delivery_fee
            totals["final_order_total"] = round(totals["total"] + delivery_fee, 2)

            # Persist order in SQLite
            order_items_payload = [
                {"product_id": it.product.product_id, "quantity": it.quantity, "unit_price": it.product.price}
                for it in cart.iter_items()
            ]
            order_id = database.save_order(
                user_id=cust.user_id,
                total_amount=totals["final_order_total"],
                tax_amount=totals["tax"],
                discount_amount=totals["discount_amount"],
                items=order_items_payload
            )

            # Generate formatted receipt & CSV
            receipt_items = [
                {"product_id": it.product.product_id, "name": it.product.name, "unit_price": it.product.price, "quantity": it.quantity, "total_price": it.total_price}
                for it in cart.iter_items()
            ]
            receipt_text = billing.generate_text_receipt(
                order_id=order_id,
                customer_name=cust.username,
                delivery_city=dest_city,
                cart_items=receipt_items,
                totals=totals
            )
            csv_path = billing.export_order_to_csv(order_id, cust.username, receipt_items, totals)

            self.send_json({
                "success": True,
                "order_id": order_id,
                "totals": totals,
                "route": {"path": route_path, "distance": distance},
                "receipt_text": receipt_text,
                "csv_path": csv_path
            })
            return

        if path == "/api/add_sku":
            name = data.get("name")
            cat = data.get("category")
            price = float(data.get("price", 0))
            stock = int(data.get("stock", 0))
            new_id = database.add_product(name, cat, price, stock)
            self.send_json({"success": True, "product_id": new_id})
            return

        if path == "/api/update_stock":
            pid = data.get("product_id")
            delta = data.get("delta", 0)
            database.update_product_stock(pid, delta)
            self.send_json({"success": True})
            return

        if path == "/api/backup":
            mgr = backup_service.BackupManager()
            bpath = mgr.create_backup()
            self.send_json({"success": True, "backup_path": bpath})
            return

        self.send_json({"error": "Endpoint not found"}, status=404)

    def send_json(self, payload, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(payload, default=str).encode("utf-8"))

def run():
    database.init_database()
    with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), FastSpringHandler) as httpd:
        print(f"[*] FastSpring Digital Invoicing Web App running on http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
