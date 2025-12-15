"""
MODULE: db.py
PURPOSE: Manages the SQLite database for logging classification history.
TECHNIQUES:
- 'sqlite3': Standard Python library for lightweight SQL databases.
- Context Managers: Uses connection objects to safely execute queries.
- Schema Definition: Checks and creates tables if they don't exist (migrations).
"""
import sqlite3
from typing import Optional
from pathlib import Path
from datetime import datetime
from . import config

def get_connection():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(config.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise

def init_db():
    """Initializes the database schema."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classification_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                from_path TEXT NOT NULL,
                to_path TEXT NOT NULL,
                document_code TEXT,
                confidence REAL,
                rationale TEXT,
                model TEXT,
                prompt_hash TEXT,
                extracted_text_chars INTEGER,
                classified_at TIMESTAMP,
                status TEXT,
                error_message TEXT
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        conn.close()

def log_event(
    filename: str,
    from_path: str,
    to_path: str,
    document_code: str,
    status: str,
    confidence: Optional[float] = None,
    rationale: Optional[str] = None,
    model: str = "",
    prompt_hash: Optional[str] = None,
    extracted_text_chars: int = 0,
    error_message: Optional[str] = None
):
    """Logs a classification event to the database."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO classification_events (
                filename, from_path, to_path, document_code, confidence, rationale,
                model, prompt_hash, extracted_text_chars, classified_at, status, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            filename, str(from_path), str(to_path), document_code, confidence, rationale,
            model, prompt_hash, extracted_text_chars, datetime.now().isoformat(), status, error_message
        ))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error logging event: {e}")
        raise  # Critical error if we can't log
    finally:
        conn.close()

def get_recent_events(limit: int = 20):
    """Retrieves recent classification events."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM classification_events ORDER BY id DESC LIMIT ?', (limit,))
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()
