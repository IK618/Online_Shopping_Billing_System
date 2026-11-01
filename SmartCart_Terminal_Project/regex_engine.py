r"""
regex_engine.py
Regular Expression (Regex) Validation and Pattern Extraction Utilities

Features:
  - Python 're' module
  - Metacharacters: ^, $, ., *, +, ?, {n,m}, \d, \D, \w, \W, \s, \S, [...], (...)
  - Functions:
      - re.match(): Match from the beginning of string
      - re.search(): Search anywhere in string
      - re.fullmatch(): Complete string match
      - re.findall(): Extract all occurrences as list
      - re.finditer(): Match objects with start() and end() positions
      - re.sub(): String replacement with pattern
      - re.split(): Splitting strings across multiple delimiters
"""

import re
from typing import List, Dict, Tuple, Optional, Any


# 1. Validation Patterns
EMAIL_PATTERN = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")
INDIAN_PHONE_PATTERN = re.compile(r"^(\+91[\-\s]?)?[6-9]\d{9}$")
DATE_PATTERN = re.compile(r"\b(\d{2}-\d{2}-\d{4}|\d{4}-\d{2}-\d{2})\b")
PROMO_CODE_PATTERN = re.compile(r"^[A-Z]{3,6}\d{2,4}$")  # e.g., FESTIVE25, DIWALI50, SAVE100


def validate_email(email: str) -> bool:
    """Validates email format using re.fullmatch."""
    if not email:
        return False
    return bool(EMAIL_PATTERN.fullmatch(email.strip()))


def validate_phone(phone: str) -> bool:
    """Validates 10-digit Indian phone number."""
    if not phone:
        return False
    return bool(INDIAN_PHONE_PATTERN.fullmatch(phone.strip()))


def validate_promo_code(code: str) -> bool:
    """Validates promo discount code format (e.g. SMART20, DIWALI50)."""
    if not code:
        return False
    return bool(PROMO_CODE_PATTERN.fullmatch(code.strip().upper()))


def extract_dates_from_text(text: str) -> List[str]:
    """Extracts date strings using re.findall."""
    return DATE_PATTERN.findall(text)


def extract_phone_numbers(text: str) -> List[str]:
    """Extracts 10-digit phone numbers using re.findall."""
    return re.findall(r"\b\d{10}\b", text)


def extract_email_addresses(text: str) -> List[str]:
    """Extracts email addresses using re.findall."""
    return re.findall(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text)


def sanitize_product_search(query: str) -> str:
    """
    Cleans search input by replacing special symbols with spaces using re.sub.
    """
    return re.sub(r"[^\w\s-]", " ", query).strip()


def split_search_terms(query: str) -> List[str]:
    """
    Splits multi-keyword query using re.split across spaces, commas, semicolons.
    """
    return [token for token in re.split(r"[,;\s]+", query) if token]


def inspect_pattern_matches(pattern_str: str, text: str) -> List[Dict[str, Any]]:
    """
    Uses re.finditer to locate match offsets (start, end, text).
    """
    results = []
    pattern = re.compile(pattern_str)
    for match in pattern.finditer(text):
        results.append({
            "matched_text": match.group(),
            "start": match.start(),
            "end": match.end(),
            "span": match.span()
        })
    return results
