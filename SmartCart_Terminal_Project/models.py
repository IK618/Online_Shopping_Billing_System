"""
models.py
Object-Oriented Data Models for Online Shopping & Billing System
Demonstrates:
  - OOP: Inheritance, Polymorphism, Encapsulation, State & Identity
  - Special methods (__init__, __str__, __len__)
  - Static & Class Methods (@staticmethod, @classmethod)
  - Python Generators (yield) & Functional programming (map, lambda)
  - Number manipulation: round() (Banker's rounding) & math.trunc()
"""

import math
from datetime import datetime
from typing import List, Dict, Optional


class Product:
    """Represents a product item in inventory."""

    def __init__(self, product_id: int, name: str, category: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.__price = float(price)  # Encapsulation: Private attribute
        self.__stock = int(stock)

    # Getters and Setters demonstrating encapsulation
    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float):
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.__price = float(new_price)

    @property
    def stock(self) -> int:
        return self.__stock

    def decrement_stock(self, quantity: int) -> bool:
        """Reduces stock upon purchase."""
        if quantity <= self.__stock:
            self.__stock -= quantity
            return True
        return False

    def restock(self, quantity: int):
        self.__stock += quantity

    def __str__(self) -> str:
        return f"[{self.product_id}] {self.name} ({self.category}) - ₹{self.__price:.2f} | Stock: {self.__stock}"


class User:
    """Base User class demonstrating OOP Inheritance."""

    def __init__(self, user_id: int, username: str, email: str, role: str = "customer"):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.role = role

    def get_role_description(self) -> str:
        return f"System User: {self.username} ({self.role})"


class Customer(User):
    """Customer subclass inheriting from User (Inheritance & Polymorphism)."""

    def __init__(self, user_id: int, username: str, email: str, city: str, is_premium: bool = False):
        super().__init__(user_id, username, email, role="customer")
        self.city = city
        self.is_premium = is_premium

    def get_discount_rate(self) -> float:
        """Polymorphism: Customer specific discount."""
        return 0.10 if self.is_premium else 0.02


class Admin(User):
    """Admin subclass inheriting from User."""

    def __init__(self, user_id: int, username: str, email: str):
        super().__init__(user_id, username, email, role="admin")

    def get_role_description(self) -> str:
        return f"Store Administrator: {self.username}"


class CartItem:
    """Represents an item placed into the ShoppingCart."""

    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    @property
    def total_price(self) -> float:
        return self.product.price * self.quantity


class ShoppingCart:
    """Shopping Cart managing customer items and calculating totals."""

    def __init__(self, customer: Customer):
        self.customer = customer
        self.items: Dict[int, CartItem] = {}

    def add_item(self, product: Product, quantity: int = 1) -> bool:
        if quantity <= 0:
            return False
        if product.product_id in self.items:
            self.items[product.product_id].quantity += quantity
        else:
            self.items[product.product_id] = CartItem(product, quantity)
        return True

    def remove_item(self, product_id: int) -> bool:
        if product_id in self.items:
            del self.items[product_id]
            return True
        return False

    def clear(self):
        self.items.clear()

    def __len__(self) -> int:
        return sum(item.quantity for item in self.items.values())

    # Generator function demonstrating `yield` (Session 7)
    def iter_items(self):
        """Generator yielding cart items one by one."""
        for item in self.items.values():
            yield item

    def calculate_subtotal(self) -> float:
        # Functional programming with map & lambda (Session 7)
        item_totals = list(map(lambda item: item.total_price, self.items.values()))
        return sum(item_totals)

    def calculate_totals(self, tax_rate: float = 0.05):
        """
        Calculates subtotal, discount, tax, and final amount.
        Demonstrates Banker's rounding and math.trunc (Session 1).
        """
        subtotal = self.calculate_subtotal()
        discount_rate = self.customer.get_discount_rate()
        discount_amount = subtotal * discount_rate
        taxable_amount = subtotal - discount_amount
        tax = taxable_amount * tax_rate
        total = taxable_amount + tax

        # Banker's rounding (standard in Python round())
        rounded_total = round(total, 2)
        # Truncated rupee integer for invoice display
        integer_rupees = math.trunc(rounded_total)

        return {
            "subtotal": round(subtotal, 2),
            "discount_rate": discount_rate,
            "discount_amount": round(discount_amount, 2),
            "tax": round(tax, 2),
            "total": rounded_total,
            "integer_rupees": integer_rupees
        }
