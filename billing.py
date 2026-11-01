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
                          cart_items: List[Dict[str, Any]], totals: Dict[str, Any],
                          shop_info: Optional[Dict[str, Any]] = None,
                          cashier_name: Optional[str] = None,
                          customer_phone: Optional[str] = None) -> str:
    """
    Creates a neatly formatted ASCII invoice using String alignment methods.
    Features billEX multi-tenant store branding and cashier attribution.
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")

    w = 62
    line = "=" * w
    subline = "-" * w

    shop_name = (shop_info.get("shop_name") if shop_info else "Apex Electronics & Retail").upper()
    shop_addr = shop_info.get("address") if shop_info else "Shop #14, Brigade Road, Bengaluru - 560001"
    gstin = shop_info.get("gstin") if shop_info else "29ABCDE1234F1Z5"
    phone = shop_info.get("phone") if shop_info else "+91 9876543210"

    receipt = []
    receipt.append(line)
    receipt.append("billEX POINT OF SALE & DIGITAL INVOICE".center(w))
    receipt.append(shop_name.center(w))
    if shop_addr:
        receipt.append(shop_addr[:w].center(w))
    receipt.append(f"GSTIN: {gstin} | Phone: {phone}".center(w))
    receipt.append(line)
    receipt.append(f"INVOICE #: SALES-{order_id:<12} DATE: {date_str}")
    receipt.append(f"CUSTOMER : {customer_name:<20} CITY: {delivery_city}")
    if cashier_name or customer_phone:
        cashier_disp = f"BILLED BY: {cashier_name or 'Store POS'}"
        phone_disp = f"PHONE: {customer_phone}" if customer_phone else ""
        receipt.append(f"{cashier_disp:<36} {phone_disp}")
    receipt.append(subline)
    receipt.append(f"{'Item Name':<32}{'Qty':<6}{'Unit Price':<12}{'Total':<12}")
    receipt.append(subline)

    for item in cart_items:
        name = item["name"][:30]  # Truncate if too long
        qty = str(item["quantity"])
        rate = f"INR {item['unit_price']:.2f}"
        tot = f"INR {item['total_price']:.2f}"
        receipt.append(f"{name:<32}{qty:<6}{rate:<12}{tot:<12}")

    receipt.append(subline)
    receipt.append(f"{'Subtotal:':<42}INR {totals['subtotal']:>12.2f}")
    discount_pct = int(totals.get('discount_rate', 0.10) * 100)
    receipt.append(f"{f'Discount ({discount_pct}%):':<42}-INR {totals['discount_amount']:>11.2f}")
    receipt.append(f"{'GST / Tax (5%):':<42}INR {totals['tax']:>12.2f}")
    if totals.get('delivery_fee', 0) > 0:
        receipt.append(f"{'Delivery / Freight:':<42}INR {totals['delivery_fee']:>12.2f}")
    receipt.append(line)
    receipt.append(f"{'NET PAYABLE TOTAL:':<42}INR {totals.get('final_order_total', totals['total']):>12.2f}")
    receipt.append(f"{'Rounded Rupee Value:':<42}INR {totals['integer_rupees']:>12d}")
    receipt.append(line)
    store_signoff = f"Thank you for shopping at {shop_info.get('shop_name', 'Apex Electronics')}!" if shop_info else "Thank you for your business!"
    receipt.append(store_signoff.center(w))
    receipt.append("Powered by billEX POS Cloud Engine".center(w))
    receipt.append(line)

    content = "\n".join(receipt)

    # Save to text file using File I/O
    file_path = os.path.join(INVOICE_DIR, f"invoice_{order_id}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return content


def export_order_to_csv(order_id: int, customer_name: str, delivery_city: str,
                        cart_items: List[Dict[str, Any]], totals: Dict[str, Any],
                        shop_info: Optional[Dict[str, Any]] = None,
                        cashier_name: Optional[str] = None) -> str:
    """
    Exports the invoice breakdown into a CSV file with billEX store headers.
    Demonstrates Session 3: csv module (csv.writer, with open).
    """
    csv_file_path = os.path.join(INVOICE_DIR, f"invoice_{order_id}.csv")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    shop_title = shop_info.get("shop_name", "Apex Electronics & Retail") if shop_info else "Apex Electronics & Retail"
    shop_addr = shop_info.get("address", "") if shop_info else ""
    gstin = shop_info.get("gstin", "") if shop_info else ""

    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Header section
        writer.writerow(["billEX Point of Sale System - Tax Invoice"])
        writer.writerow(["Store Name", shop_title, "GSTIN", gstin])
        writer.writerow(["Store Address", shop_addr])
        writer.writerow(["Order ID", f"SALES-{order_id}", "Date", timestamp])
        writer.writerow(["Customer", customer_name, "Destination City", delivery_city])
        if cashier_name:
            writer.writerow(["Billed By", cashier_name])
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

        writer.writerow([])
        writer.writerow(["Subtotal", f"{totals['subtotal']:.2f}"])
        writer.writerow(["Discount", f"-{totals['discount_amount']:.2f}"])
        writer.writerow(["GST Tax (5%)", f"{totals['tax']:.2f}"])
        if totals.get('delivery_fee', 0) > 0:
            writer.writerow(["Delivery Freight", f"{totals['delivery_fee']:.2f}"])
        writer.writerow(["Total Amount", f"{totals.get('final_order_total', totals['total']):.2f}"])

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
