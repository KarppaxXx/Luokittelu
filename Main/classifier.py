"""
MODULE: classifier.py
PURPOSE: Orchestrates the entire classification workflow (Load -> Extract -> Classify -> Move).
TECHNIQUES:
- Logic Flow: Connects all other modules (db, pdf_extract, llm) into a single process.
- Error Handling: Wraps major steps in try-except blocks to prevent crashes on bad files.
- Transactional Logic: Ensures database logging happens alongside file operations.
"""
from pathlib import Path
from rich.console import Console
from . import config, db, pdf_extract, llm_client, filesystem, instructions_loader, utils

console = Console()

def process_all_files():
    """Main workflow to process all unclassified files."""
    
    # 1. Load instructions
    try:
        doc_types = instructions_loader.load_document_types()
        console.print(f"[green]Loaded {len(doc_types)} document types.[/green]")
    except Exception as e:
        console.print(f"[bold red]Error loading instructions:[/bold red] {e}")
        return

    # 2. List files
    pdfs = filesystem.get_unclassified_pdfs()
    if not pdfs:
        console.print("[yellow]No PDF files found in Doc directory.[/yellow]")
        return
    
    console.print(f"[bold cyan]Found {len(pdfs)} unclassified PDFs.[/bold cyan]")

    for pdf in pdfs:
        console.print(f"\n[bold]Processing:[/bold] {pdf.name}")
        
        # 3. Extract Text
        text = pdf_extract.extract_text(pdf)
        extracted_chars = len(text) if text else 0
        
        prompt_hash = utils.calculate_hash(text) if text else None

        if not text:
            console.print("  [red]No text extracted. Marking as NO_TEXT_NO_OCR.[/red]")
            db.log_event(
                filename=pdf.name,
                from_path=str(pdf),
                to_path="",
                document_code="UNKNOWN",
                status="NO_TEXT_NO_OCR",
                error_message="Text extraction returned nothing (OCR skipped per config)."
            )
            continue
            
        # 4. Classify with LLM
        console.print(f"  Extracted {extracted_chars} chars. Sending to OpenAI...")
        try:
            result = llm_client.classify_document(text, doc_types)
            console.print(f"  [green]Result:[/green] {result['document_code']} (Conf: {result['confidence']})")
        except Exception as e:
            console.print(f"  [bold red]Classification failed:[/bold red] {e}")
            db.log_event(
                filename=pdf.name,
                from_path=str(pdf),
                to_path="",
                document_code="",
                status="ERROR",
                extracted_text_chars=extracted_chars,
                error_message=str(e)
            )
            continue

        # 5. Move File
        target_dir = config.DOC_DIR / result['document_code']
        try:
            final_path = filesystem.move_file(pdf, target_dir)
            console.print(f"  [cyan]Moved to:[/cyan] {final_path}")
            
            # 6. Log Success
            db.log_event(
                filename=pdf.name,
                from_path=str(pdf),
                to_path=str(final_path),
                document_code=result['document_code'],
                status="OK",
                confidence=result['confidence'],
                rationale=result['rationale'],
                model=config.OPENAI_MODEL,
                prompt_hash=prompt_hash,
                extracted_text_chars=extracted_chars
            )
        except Exception as e:
            console.print(f"  [bold red]File move failed:[/bold red] {e}")
            # Log critical error but don't delete anything
            db.log_event(
                filename=pdf.name,
                from_path=str(pdf),
                to_path="",
                document_code=result['document_code'],
                status="ERROR",
                error_message=f"Move failed: {e}"
            )

    console.print("\n[bold green]Batch processing complete.[/bold green]")
