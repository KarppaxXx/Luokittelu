# PDF Classifier

An automated tool to classify PDF documents using OpenAI's LLM based on user-defined categories.

## Features
- **Automatic Text Extraction**: Prioritizes "digital-born" text.
- **AI Classification**: Uses OpenAI to categorize documents.
- **Excel Configuration**: Define your own document types and codes easily.
- **SQLite Logging**: Tracks every classification event.
- **CLI Interface**: Simple menu-driven control.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file in the project root with your API key:
   ```env
   OPENAI_API_KEY=sk-...
   ```
   (Or set it in your system environment)

3. **Document Types**
   Edit `instructions/document_types.xlsx`. 
   Required columns: `code`, `title`, `description`.

## Usage

1. **Place PDF files** to be classified into the `Doc/` folder.

2. **Run the Classifier**
   ```bash
   python Main/app.py
   ```

3. **Follow the Menu**
   - Select `1` to process files.
   - Select `7` to check system health.

## Directory Structure
- `Doc/` - Input PDFs (and Output subdirectories)
- `instructions/` - Excel rules
- `Database/` - Logs
- `Main/` - Source code

## Notes
- Files with no extractable text will be marked `NO_TEXT_NO_OCR` and skipped.
- Failed classifications are safe; files are not moved if an error occurs.
