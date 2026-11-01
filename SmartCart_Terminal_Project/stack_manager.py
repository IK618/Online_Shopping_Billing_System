"""
stack_manager.py
Stack Data Structure Implementation & Applications

Implements:
  - Stack linear data structure (LIFO: Last-In, First-Out)
  - Custom Stack class implementation (items list, push, pop, peep, is_empty, size)
  - Optimized Stack implementation using collections.deque
  - Applications:
      1. String Reversal using Stack
      2. Parentheses & Brackets Matching / Balance Verification
      3. Shopping Cart Undo / History Manager
  - Time Complexity: O(1) for push, pop, peep, is_empty
"""

from collections import deque
from typing import Any, List, Optional, Tuple


class Stack:
    """Standard Stack implementation using a Python list."""

    def __init__(self):
        self.items: List[Any] = []

    def push(self, item: Any) -> None:
        """Pushes an element onto the top of the stack. O(1)."""
        self.items.append(item)

    def pop(self) -> Any:
        """Removes and returns the top element of the stack. O(1)."""
        if not self.is_empty():
            return self.items.pop()
        return None

    def peep(self) -> Any:
        """Views the top element without removing it. O(1)."""
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self) -> bool:
        """Checks if the stack is empty."""
        return len(self.items) == 0

    def size(self) -> int:
        """Returns the number of elements in the stack."""
        return len(self.items)

    def to_list(self) -> List[Any]:
        """Returns a snapshot copy of the stack items."""
        return self.items.copy()

    def __str__(self) -> str:
        return f"Stack({self.items})"


class DequeStack:
    """Optimized Stack implementation using collections.deque."""

    def __init__(self):
        self._deque = deque()

    def push(self, item: Any) -> None:
        self._deque.append(item)

    def pop(self) -> Any:
        if self._deque:
            return self._deque.pop()
        return None

    def peep(self) -> Any:
        if self._deque:
            return self._deque[-1]
        return None

    def is_empty(self) -> bool:
        return len(self._deque) == 0

    def size(self) -> int:
        return len(self._deque)


def reverse_string_using_stack(text: str) -> str:
    """Reverses a string using a Stack."""
    stack = Stack()
    for ch in text:
        stack.push(ch)
    reversed_str = ""
    while not stack.is_empty():
        reversed_str += stack.pop()
    return reversed_str


def is_parentheses_balanced(expr: str) -> bool:
    """
    Checks whether brackets in an expression are balanced.
    Supports '()', '[]', and '{}'.
    """
    stack = Stack()
    matching = {')': '(', ']': '[', '}': '{'}
    opening = set(matching.values())

    for ch in expr:
        if ch in opening:
            stack.push(ch)
        elif ch in matching:
            if stack.is_empty():
                return False
            top = stack.pop()
            if top != matching[ch]:
                return False

    return stack.is_empty()


class CartAction:
    """Encapsulates a user action on the shopping cart for Undo operations."""

    def __init__(self, action_type: str, product_id: int, product_name: str, quantity: int, unit_price: float):
        self.action_type = action_type  # 'ADD' or 'REMOVE'
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price

    def __str__(self) -> str:
        return f"[{self.action_type}] {self.quantity}x {self.product_name} (ID: {self.product_id})"


class CartHistoryManager:
    """Manages undo history for the shopping cart using a LIFO Stack."""

    def __init__(self):
        self._undo_stack = Stack()

    def record_add(self, product_id: int, product_name: str, quantity: int, unit_price: float) -> None:
        action = CartAction("ADD", product_id, product_name, quantity, unit_price)
        self._undo_stack.push(action)

    def record_remove(self, product_id: int, product_name: str, quantity: int, unit_price: float) -> None:
        action = CartAction("REMOVE", product_id, product_name, quantity, unit_price)
        self._undo_stack.push(action)

    def can_undo(self) -> bool:
        return not self._undo_stack.is_empty()

    def pop_last_action(self) -> Optional[CartAction]:
        return self._undo_stack.pop()

    def peek_last_action(self) -> Optional[CartAction]:
        return self._undo_stack.peep()

    def history_depth(self) -> int:
        return self._undo_stack.size()
