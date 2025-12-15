"""
MODULE: app.py
PURPOSE: Serves as the main entry point and Command Line Interface (CLI) for the user.
TECHNIQUES:
- Uses 'rich' library for beautiful, colored terminal output and tables.
- Implements a while-loop for a persistent menu system.
- Handles user input securely and routes actions to other modules.
"""
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from . import config, db, classifier, filesystem

console = Console()

def show_menu():
    """Displays the main menu."""
    console.print(Panel.fit("[bold blue]PDF Classifier CLI[/bold blue]"))
    print("1. Run automatic classification")
    print("2. List unclassified PDFs")
    print("3. List NO_TEXT_NO_OCR files")
    print("4. View classification history")
    print("5. Reload document types (Check Excel)")
    print("6. Settings")
    print("7. Health check")
    print("0. Exit")

def list_unclassified():
    pdfs = filesystem.get_unclassified_pdfs()
    if not pdfs:
        console.print("[yellow]No unclassified files found.[/yellow]")
    else:
        table = Table(title="Unclassified PDFs")
        table.add_column("Filename", style="cyan")
        table.add_column("Size (KB)", justify="right")
        for pdf in pdfs:
            size_kb = pdf.stat().st_size / 1024
            table.add_row(pdf.name, f"{size_kb:.1f}")
        console.print(table)

def show_history():
    events = db.get_recent_events()
    if not events:
        console.print("[yellow]No history found.[/yellow]")
        return
        
    table = Table(title="Recent Activity")
    table.add_column("Time", style="dim")
    table.add_column("File")
    table.add_column("Action")
    table.add_column("Status")
    
    for e in events:
        action = f"{e['document_code']} ({int((e['confidence'] or 0)*100)}%)"
        status_style = "green" if e['status'] == 'OK' else "red"
        table.add_row(
            e['classified_at'][:19], 
            e['filename'], 
            action, 
            f"[{status_style}]{e['status']}[/{status_style}]"
        )
    console.print(table)

def health_check():
    console.print("[bold]Checking system health...[/bold]")
    
    # Dirs
    for d in [config.DOC_DIR, config.DATABASE_DIR, config.INSTRUCTIONS_DIR]:
        status = "[green]OK[/green]" if d.exists() else "[red]MISSING[/red]"
        console.print(f"Directory {d.name}: {status}")
        
    # DB
    try:
        db.init_db()
        console.print("Database: [green]Connected[/green]")
    except Exception as e:
        console.print(f"Database: [red]Error - {e}[/red]")
        
    # Excel
    if config.INSTRUCTIONS_FILE.exists():
        console.print("Excel Instructions: [green]Found[/green]")
    else:
        console.print("Excel Instructions: [red]Missing[/red]")

    # API Key
    if config.OPENAI_API_KEY:
        console.print("OpenAI API Key: [green]Present[/green]")
    else:
        console.print("OpenAI API Key: [red]Missing[/red] (Check environment variables)")

def run():
    # Ensure DB exists
    db.init_db()
    
    while True:
        print()
        show_menu()
        choice = input("\nSelect an option: ").strip()
        
        if choice == '1':
            classifier.process_all_files()
        elif choice == '2':
            list_unclassified()
        elif choice == '3':
            console.print("[dim]Feature 'List NO_TEXT_NO_OCR files' not fully implemented separate view, check History.[/dim]")
            # Implementation shorthand: query DB for this status
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT filename, classified_at FROM classification_events WHERE status='NO_TEXT_NO_OCR' ORDER BY id DESC LIMIT 10")
            rows = cursor.fetchall()
            if not rows:
                console.print("[green]No files found with NO_TEXT_NO_OCR status.[/green]")
            for r in rows:
                console.print(f"- {r['filename']} ({r['classified_at']})")
            conn.close()

        elif choice == '4':
            show_history()
        elif choice == '5':
            # Instructions are reloaded on every run, but we can verify it here
            try:
                from . import instructions_loader
                types = instructions_loader.load_document_types()
                console.print(f"[green]Successfully read Excel. Found {len(types)} definitions.[/green]")
            except Exception as e:
                console.print(f"[red]Error reading Excel: {e}[/red]")
        elif choice == '6':
            console.print(Panel(f"""
            [bold]Current Settings:[/bold]
            Model: {config.OPENAI_MODEL}
            Temp: {config.OPENAI_TEMPERATURE}
            Max Text: {config.MAX_TEXT_LENGTH} chars
            Retry: {config.RETRY_ATTEMPTS} attempts
            Note: Edit config.py to change these.
            """))
        elif choice == '7':
            health_check()
        elif choice == '0':
            console.print("Goodbye!")
            break
        else:
            console.print("[red]Invalid option.[/red]")

if __name__ == "__main__":
    run()
