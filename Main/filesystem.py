"""
MODULE: filesystem.py
PURPOSE: Handles physical file operations like listing and moving files.
TECHNIQUES:
- 'pathlib': Object-oriented filesystem paths.
- 'shutil': High-level file operations (move).
- Conflict Resolution: Logic to detect if a file exists and rename it (file_1.pdf) to avoid overwriting.
"""
import shutil
from pathlib import Path
from typing import List
from . import config

def get_unclassified_pdfs() -> List[Path]:
    """List all PDF files in the Doc directory (root only)."""
    return [
        p for p in config.DOC_DIR.iterdir() 
        if p.is_file() and p.suffix.lower() == '.pdf'
    ]

def move_file(source: Path, destination_dir: Path) -> Path:
    """
    Moves a file to the destination directory.
    Handles naming conflicts by appending a counter.
    Returns the final path of the moved file.
    """
    if not destination_dir.exists():
        destination_dir.mkdir(parents=True, exist_ok=True)

    destination_file = destination_dir / source.name
    
    # Handle conflicts
    if destination_file.exists():
        stem = source.stem
        suffix = source.suffix
        counter = 1
        while destination_file.exists():
            destination_file = destination_dir / f"{stem}_{counter}{suffix}"
            counter += 1
            
    shutil.move(str(source), str(destination_file))
    return destination_file
