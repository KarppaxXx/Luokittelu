"""
MODULE: models.py
PURPOSE: Defines strict data structures (types) used across the app.
TECHNIQUES:
- 'TypedDict': Enforces specific keys and types for dictionaries (Code, Title, Description).
- Type Hinting: Helps code editors (IDE) catch errors before running the code.
"""
from typing import TypedDict, Optional, List

class DocumentType(TypedDict):
    code: str
    title: str
    description: str

class ClassificationResult(TypedDict):
    document_code: str
    confidence: float
    rationale: str
