"""
billing.py
Invoicing, CSV Export, and SMTP Email Notification Service
Demonstrates:
  - Session 1: datetime.now(), strftime() format codes
  - Session 3: File I/O (with open, modes 'w', 'a'), writing multiple lines
  - Session 3: CSV generation using csv module (csv.writer)
  - Session 6: String methods (ljust, rjust, center, strip, formatting)
  - Session 9: smtplib (SMTP, port 587, starttls, EmailMessage, attachments)
"""

import os
import csv
import smtplib
from email.message import EmailMessage
from datetime import datetime
from typing import Dict, Any, List

INVOICE_DIR = os.path.join(os.path.dirname(__file__), "invoices")
os.makedirs(INVOICE_DIR, exist_ok=True)


def generate_text_receipt(order_id: int, customer_name: str, delivery_city: str,
                          cart_items: List[Dict[str, Any]], totals: Dict[str, Any]) -> str:
    """
    Creates a neatly formatted ASCII invoice using String alignment methods.
    Demonstrates: ljust, rjust, center, format codes.
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")

    line = "=" * 55
    subline = "-" * 55

    receipt = []
    receipt.append(line)
    receipt.append("SMARTCART ONLINE RETAIL STORE".center(55))
    receipt.append("TAX INVOICE & CASH RECEIPT".center(55))
    receipt.append(line)
    receipt.append(f"Invoice ID : #{order_id:<10} Date: {date_str}")
    receipt.append(f"Customer   : {customer_name:<20} City: {delivery_city}")
    receipt.append(subline)
    receipt.append(f"{'Item Name':<28}{'Qty':<6}{'Rate':<10}{'Total':<10}")
    receipt.append(subline)

    for item in cart_items:
        name = item["name"][:26]  # Truncate if too long
        qty = str(item["quantity"])
        rate = f"₹{item['unit_price']:.2f}"
        tot = f"₹{item['total_price']:.2f}"
        receipt.append(f"{name:<28}{qty:<6}{rate:<10}{tot:<10}")

    receipt.append(subline)
    receipt.append(f"{'Subtotal:':<40}₹{totals['subtotal']:>10.2f}")
    discount_pct = int(totals['discount_rate'] * 100)
    receipt.append(f"{f'Discount ({discount_pct}%):':<40}-₹{totals['discount_amount']:>9.2f}")
    receipt.append(f"{'GST / Tax (5%):':<40}₹{totals['tax']:>10.2f}")
    receipt.append(line)
    receipt.append(f"{'NET PAYABLE TOTAL:':<40}₹{totals['total']:>10.2f}")
    receipt.append(f"{'Rounded Rupee Value:':<40}₹{totals['integer_rupees']:>10d}")
    receipt.append(line)
    receipt.append("Thank you for shopping with SmartCart!".center(55))
    receipt.append("For queries contact: support@smartcart.com".center(55))
    receipt.append(line)

    content = "\n".join(receipt)

    # Save to text file using File I/O
    file_path = os.path.join(INVOICE_DIR, f"invoice_{order_id}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return content


def export_order_to_csv(order_id: int, customer_name: str, delivery_city: str,
                        cart_items: List[Dict[str, Any]], totals: Dict[str, Any]) -> str:
    """
    Exports the invoice breakdown into a CSV file.
    Demonstrates Session 3: csv module (csv.writer, with open).
    """
    csv_file_path = os.path.join(INVOICE_DIR, f"invoice_{order_id}.csv")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Header section
        writer.writerow(["SmartCart Retail Invoicing System"])
        writer.writerow(["Order ID", order_id, "Date", timestamp])
        writer.writerow(["Customer", customer_name, "Destination City", delivery_city])
        writer.writerow([])  # Blank row

        # Table header
        writer.writerow(["Product ID", "Product Name", "Quantity", "Unit Price (INR)", "Total Price (INR)"])

        # Table rows
        for item in cart_items:
            writer.writerow([
                item["product_id"],
                item["name"],
                item["quantity"],
                f"{item['unit_price']:.2f}",
                f"{item['total_price']:.2f}"
            ])

        # Summary rows
        writer.writerow([])
        writer.writerow(["", "", "", "Subtotal", f"{totals['subtotal']:.2f}"])
        writer.writerow(["", "", "", "Discount", f"-{totals['discount_amount']:.2f}"])
        writer.writerow(["", "", "", "GST Tax", f"{totals['tax']:.2f}"])
        writer.writerow(["", "", "", "Grand Total", f"{totals['total']:.2f}"])

    return csv_file_path


def send_invoice_email(recipient_email: str, order_id: int, invoice_text: str,
                       smtp_user: str = "", smtp_pass: str = "") -> bool:
    """
    Sends an automated email invoice using smtplib (Session 9).
    If SMTP credentials are not configured, prints a simulation log for testing.
    """
    if not smtp_user or not smtp_pass:
        print(f"[SMTP Simulation] Invoice email queued for {recipient_email} (Order #{order_id}).")
        return True

    try:
        msg = EmailMessage()
        msg["Subject"] = f"Your SmartCart Order Confirmation & Receipt #{order_id}"
        msg["From"] = smtp_user
        msg["To"] = recipient_email
        msg.set_content(invoice_text)

        # Attach the CSV invoice
        csv_path = os.path.join(INVOICE_DIR, f"invoice_{order_id}.csv")
        if os.path.exists(csv_path):
            with open(csv_path, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="text",
                    subtype="csv",
                    filename=f"invoice_{order_id}.csv"
                )

        # Connect to Gmail / standard TLS SMTP on port 587
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        print(f"[SMTP Success] Invoice successfully sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"[SMTP Notice] Could not send live email: {e}")
        return False
