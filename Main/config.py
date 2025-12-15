"""
MODULE: config.py
PURPOSE: Centralizes configuration settings and file paths.
TECHNIQUES:
- 'pathlib': For robust, cross-platform file path handling (works on Windows/Mac/Linux).
- 'dotenv': Loads secrets (API keys) from a hidden .env file to keep them secure.
- Constants: Uses UPPER_CASE variables for global settings easy to change.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DOC_DIR = BASE_DIR / "Doc"
DATABASE_DIR = BASE_DIR / "Database"
INSTRUCTIONS_DIR = BASE_DIR / "instructions"

# File Paths
DB_PATH = DATABASE_DIR / "classification_events.db"
INSTRUCTIONS_FILE = INSTRUCTIONS_DIR / "document_types.xlsx"

# OpenAI Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"  # Default model
OPENAI_TEMPERATURE = 0.0
MAX_TEXT_LENGTH = 10000  # Characters to send to LLM

# App Settings
RETRY_ATTEMPTS = 3
RETRY_BACKOFF_BASE = 2
