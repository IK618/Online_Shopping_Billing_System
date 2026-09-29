"""
network_pos.py
Client-Server Network POS Terminal
Demonstrates Session 9:
  - Python socket module
  - AF_INET, SOCK_STREAM
  - bind(), listen(), accept(), connect(), send(), recv(), close()
"""

import socket
import threading
import json
import time

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 65432


def start_pos_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    """
    Runs a TCP Socket Server that listens for remote Cashier transactions.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow port reuse
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"[POS Server] Listening for Cashier terminals on {host}:{port}...")

        while True:
            client_conn, client_addr = server_socket.accept()
            print(f"[POS Server] Connection accepted from {client_addr}")
            
            # Receive transaction payload
            data = client_conn.recv(4096).decode("utf-8")
            if data:
                payload = json.loads(data)
                print(f"[POS Server] Received Order from Cashier: {payload.get('customer')}, Total: ₹{payload.get('total')}")
                response = {"status": "SUCCESS", "message": "Transaction verified and recorded."}
                client_conn.sendall(json.dumps(response).encode("utf-8"))

            client_conn.close()
    except Exception as e:
        print(f"[POS Server Error]: {e}")
    finally:
        server_socket.close()


def send_pos_transaction(payload: dict, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> dict:
    """
    Socket Client that sends an order transaction to the central POS server.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        client_socket.sendall(json.dumps(payload).encode("utf-8"))
        raw_response = client_socket.recv(4096).decode("utf-8")
        return json.loads(raw_response)
    except ConnectionRefusedError:
        return {"status": "OFFLINE", "message": "Central POS Server is offline (Local mode active)."}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
    finally:
        client_socket.close()


if __name__ == "__main__":
    # Test script: launch server in thread and send test payload
    server_thread = threading.Thread(target=start_pos_server, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    test_order = {"customer": "Test Cashier", "total": 2999.0, "items": 2}
    print("[Client] Sending test transaction...")
    result = send_pos_transaction(test_order)
    print(f"[Client] Response: {result}")
