"""
MODULE: create_sample_excel.py
PURPOSE: A setup script to generate a template Excel file for the user.
TECHNIQUES:
- 'pandas': Used to create a DataFrame and export it directly to an .xlsx file.
- Directory Creation: Ensures the folder exists before writing the file.
"""
import pandas as pd
from pathlib import Path

# Path to the file
target_path = Path("instructions/document_types.xlsx")
target_path.parent.mkdir(parents=True, exist_ok=True)

data = [
    {"code": "INV", "title": "Invoice", "description": "A bill or invoice for payment."},
    {"code": "CTR", "title": "Contract", "description": "A legal contract or agreement between parties."},
    {"code": "REP", "title": "Report", "description": "A technical or business report."},
    {"code": "RES", "title": "Resume", "description": "A CV or resume of a job applicant."}
]

if not target_path.exists():
    df = pd.DataFrame(data)
    df.to_excel(target_path, index=False)
    print(f"Created sample Excel file at {target_path}")
else:
    print(f"File already exists at {target_path}, skipping creation.")
