"""
MODULE: utils.py
PURPOSE: Small helper functions used in multiple places.
TECHNIQUES:
- 'hashlib': Creates a unique fingerprint (SHA256) of text content to track duplicates or changes.
"""
import hashlib

def calculate_hash(text: str) -> str:
    """Calculates SHA256 hash of the input text."""
    if not text:
        return ""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()
