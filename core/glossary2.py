import pandas as pd

def check_against_glossary(terms_df, glossary):
    # Normalize glossary terms
    glossary_map = {
        str(row["EN"]).strip().lower(): str(row["Italian"]).strip()
        for _, row in glossary.iterrows()
    }

    in_gloss = []
    italian_terms = []
    notes = []

    for term in terms_df["Term (EN)"]:
        norm_term = term.strip().lower()
        if norm_term in glossary_map:
            in_gloss.append("Yes")
            italian_terms.append(glossary_map[norm_term])
        else:
            in_gloss.append("No")
            italian_terms.append("")
        notes.append("")  # Reserved for future use

    terms_df["In Glossary?"] = in_gloss
    terms_df["Term (Italian)"] = italian_terms
    terms_df["Notes"] = notes

    return terms_df
