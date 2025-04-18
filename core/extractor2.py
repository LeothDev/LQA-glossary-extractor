import spacy
from collections import Counter, defaultdict
import pandas as pd
from tqdm import tqdm

nlp = spacy.load("en_core_web_sm")

def extract_terms(df, max_ngram_length=5, min_freq=10):
    terms = Counter()
    contexts = defaultdict(list)

    # tqdm over DataFrame rows
    print("[1/2] Extracting noun chunks...")
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing strings", unit="row"):
        en_text = str(row["EN"])
        it_text = str(row["Italian"])

        doc = nlp(en_text)
        for chunk in doc.noun_chunks:
            term = chunk.text.strip().lower()
            if 1 <= len(term.split()) <= max_ngram_length:
                if not any(tok.is_stop or tok.is_punct or tok.is_digit for tok in chunk):
                    terms[term] += 1
                    contexts[term].append((en_text, it_text))

    # Convert to DataFrame
    print("[2/2] Building output...")
    term_data = []
    for term, freq in tqdm(terms.items(), desc="Filtering terms", unit="term"):
        if freq >= min_freq:
            en_example, it_example = contexts[term][0]
            term_data.append({
                "Term (EN)": term,
                "Frequency": freq,
                "Example EN": en_example,
                "Example IT": it_example
            })

    return pd.DataFrame(term_data)
