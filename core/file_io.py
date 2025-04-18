import pandas as pd

def load_translation_file(path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(path, engine="openpyxl", usecols=["strId", "EN", "Italian"])
        df.dropna(subset=["EN", "Italian"], inplace=True)
        return df
    except Exception as e:
        raise Exception(f"Failed to load translation file: {e}")

def load_glossary_file(path: str) -> pd.DataFrame:
    try:
        glossary = pd.read_excel(path, engine="openpyxl", usecols=["en Term1", "it Term1"])
        glossary.rename(columns={"en Term1": "EN", "it Term1": "Italian"}, inplace=True)
        glossary.dropna(subset=["EN", "Italian"], inplace=True)
        return glossary
    except Exception as e:
        raise Exception(f"Failed to load glossary file: {e}")
