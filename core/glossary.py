def normalize(text: str) -> str:
    return text.strip().lower()

def check_against_glossary(term_en: str, glossary_df) -> bool:
    glossary_set = set(normalize(t) for t in glossary_df["EN"])
    return normalize(term_en) in glossary_set
