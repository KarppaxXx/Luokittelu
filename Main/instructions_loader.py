"""
MODULE: instructions_loader.py
PURPOSE: Reads and validates the document rules from the Excel file.
TECHNIQUES:
- 'pandas': Powerful data analysis library used here for easy Excel reading.
- Data Validation: Checks if required columns exist before processing.
- Normalization: Cleans text (strip spaces, lowercase) to ensure reliable matching.
"""
import pandas as pd
from typing import List
from . import config
from .models import DocumentType

def load_document_types() -> List[DocumentType]:
    """Loads document types from the Excel file."""
    if not config.INSTRUCTIONS_FILE.exists():
        raise FileNotFoundError(f"Instructions file not found at {config.INSTRUCTIONS_FILE}")

    try:
        df = pd.read_excel(config.INSTRUCTIONS_FILE)
        
        # Normalize columns: lower case and strip spaces
        df.columns = df.columns.astype(str).str.lower().str.strip()
        
        required_columns = {'code', 'title', 'description'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Excel file missing required columns: {required_columns - set(df.columns)}")

        # Convert to list of dictionaries
        doc_types = []
        for _, row in df.iterrows():
            if pd.isna(row['code']):
                continue # Skip empty rows
            
            doc_types.append(DocumentType(
                code=str(row['code']).strip(),
                title=str(row['title']).strip() if not pd.isna(row['title']) else "",
                description=str(row['description']).strip() if not pd.isna(row['description']) else ""
            ))
            
        if not doc_types:
            raise ValueError("No valid document types found in Excel file.")
            
        return doc_types

    except Exception as e:
        raise Exception(f"Error loading instructions: {e}")
