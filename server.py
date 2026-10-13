#!/usr/bin/env python3
"""
server.py
Lightweight API & Frontend Server for SmartCart Retail Platform
Serves the custom high-end Web UI and REST API.
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from datetime import datetime

import database
import models
import billing
import analytics
import routing
import backup_service
import network_pos
import threading

PORT = 3000
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")



class SmartCartRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/products":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            prods = [dict(p) for p in database.get_all_products()]
            self.wfile.write(json.dumps(prods).encode("utf-8"))
            return

        elif path == "/api/categories":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            cats = database.get_product_categories()
            self.wfile.write(json.dumps(cats).encode("utf-8"))
            return

        elif path == "/api/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            mets = analytics.compute_sales_metrics()
            self.wfile.write(json.dumps(mets).encode("utf-8"))
            return

        elif path == "/api/hubs":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            optimizer = routing.LogisticsOptimizer()
            hubs = optimizer.get_all_cities()
            self.wfile.write(json.dumps(hubs).encode("utf-8"))
            return

        elif path == "/api/route":
            query = urllib.parse.parse_qs(parsed.query)
            destination = query.get("city", ["Chennai"])[0]
            optimizer = routing.LogisticsOptimizer()
            path_nodes, distance_km = optimizer.find_shortest_route(destination)
            eta_hours = round(distance_km / 60.0, 1)
            result = {
                "destination": destination,
                "origin": "Bengaluru (Hub)",
                "distance_km": distance_km,
                "eta": f"~{eta_hours} Hours",
                "path": path_nodes
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
            return


        elif path == "/api/orders":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            orders = database.get_detailed_orders(limit=25)
            self.wfile.write(json.dumps(orders).encode("utf-8"))
            return

        # Serve static web files
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/checkout":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)

            customer_name = data.get("customer_name", "Valued Customer")
            email = data.get("email", "customer@smartcart.internal")
            city = data.get("city", "Bengaluru")
            is_premium = bool(data.get("is_premium", False))
            items = data.get("items", [])

            # Build shopping cart
            customer = models.Customer(1, customer_name, email, city, is_premium)
            cart = models.ShoppingCart(customer)
            cart_items_data = []

            for it in items:
                prod = models.Product(it["product_id"], it["name"], it.get("category", "General"), float(it["price"]), int(it.get("stock", 99)))
                cart.add_item(prod, int(it["quantity"]))
                cart_items_data.append({
                    "product_id": it["product_id"],
                    "name": it["name"],
                    "quantity": int(it["quantity"]),
                    "unit_price": float(it["price"]),
                    "total_price": float(it["price"]) * int(it["quantity"])
                })

            totals = cart.calculate_totals()
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            order_id = database.save_order(
                user_id=1,
                order_date=order_date,
                subtotal=totals["subtotal"],
                discount=totals["discount_amount"],
                tax=totals["tax"],
                total=totals["total"],
                delivery_city=city,
                items=cart_items_data
            )

            receipt_text = billing.generate_text_receipt(
                order_id, customer_name, city, cart_items_data, totals
            )
            billing.export_order_to_csv(order_id, customer_name, city, cart_items_data, totals)

            resp_data = {
                "success": True,
                "order_id": order_id,
                "order_date": order_date,
                "total": totals["total"],
                "totals": totals,
                "receipt_text": receipt_text,
                "delivery_city": city
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode("utf-8"))
            return

        elif parsed.path == "/api/backup":
            worker = backup_service.run_async_backup()
            resp_data = {
                "success": True,
                "message": "Background backup thread dispatched via threading.Thread",
                "thread_name": worker.name,
                "is_alive": worker.is_alive(),
                "active_threads": threading.active_count()
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode("utf-8"))
            return

        elif parsed.path == "/api/pos_test":
            res = network_pos.send_pos_transaction({"terminal": "Web_POS_Client", "total": 4999.0, "items": 1})
            resp_data = {
                "success": True,
                "socket_protocol": "TCP/IP (AF_INET, SOCK_STREAM)",
                "target_port": network_pos.DEFAULT_PORT,
                "result": res
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode("utf-8"))
            return

        elif parsed.path == "/api/login":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            username = data.get("username", "").strip()
            password = data.get("password", "")

            user = database.authenticate_user(username, password)
            if user:
                resp_data = {
                    "success": True,
                    "user": {
                        "user_id": user["user_id"],
                        "username": user["username"],
                        "email": user["email"],
                        "city": user["city"],
                        "is_premium": bool(user["is_premium"]),
                        "role": user["role"]
                    }
                }
            else:
                resp_data = {
                    "success": False,
                    "message": "Invalid username or password. Try 'rahul_sharma' / 'pass123' or 'admin_user' / 'admin123'."
                }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode("utf-8"))
            return

        elif parsed.path == "/api/register":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            username = data.get("username", "").strip()
            password = data.get("password", "")
            email = data.get("email", "").strip()
            city = data.get("city", "Bengaluru").strip()
            is_premium = 1 if data.get("is_premium") else 0

            success, message = database.register_user(username, email, password, city, is_premium)
            resp_data = {
                "success": success,
                "message": message
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode("utf-8"))
            return

        self.send_error(404, "Endpoint not found")

def run():
    database.init_database()
    os.makedirs(WEB_DIR, exist_ok=True)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SmartCartRequestHandler) as httpd:
        print(f"SmartCart High-End Web Platform running on http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
