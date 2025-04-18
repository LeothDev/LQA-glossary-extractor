from rich.console import Console
from rich.prompt import Prompt
from core.file_io import load_translation_file, load_glossary_file
from core.extractor import extract_terms
from core.glossary import check_against_glossary
import pandas as pd

console = Console()

def main():
    console.rule("[bold cyan]GLOSSARY EXTRACTOR")
    translations_path = Prompt.ask("Enter the path to your translations Excel file", default="data/ALT-1-5-04.xlsx")
    glossary_path = Prompt.ask("Enter the path to your glossary Excel file", default="data/IT-Glossary.xlsx")

    df = load_translation_file(translations_path)
    glossary = load_glossary_file(glossary_path)

    console.print(f"[green]Loaded {len(df)} translationg strings from ALT")
    console.print(f"[green]Loaded {len(glossary)} glossary entries")

    candidates = extract_terms(df, glossary)
    console.print(f"[yellow]Extracted {len(candidates)} candidate terms")

    output_path = "output/ZGAME-Glossary-Candidates.xlsx"
    candidates.to_excel(output_path, index=False)
    console.print(f"[bold green]Glossary candidate file saved at: {output_path}")

if __name__ == "__main__":
    main()
    # df = load_translation_file("data/ALT-1-5-04.xlsx")
    # print(df.head())

    
