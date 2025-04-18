import pandas as pd
from collections import Counter, defaultdict
import re
from nltk import ngrams
from nltk.tokenize import word_tokenize
from core.glossary import check_against_glossary

def preprocess_text(text: str) -> list[str]:
    text = re.sub(r"<.*?>", "", text) # Remove tags
    text = re.sub(r"[^\w\s]", "", text)# Remove punctuation
    text = text.lower() 
    return word_tokenize(text)

def get_ngram_frequencies(df: pd.DataFrame, n_range=(1,5), min_freq: int = 5) -> Counter:
    counter = Counter()

    for text in df["EN"]:
        tokens = preprocess_text(text)
        for n in range(n_range[0], n_range[1]+1):
            for gram in ngrams(tokens, n):
                counter[" ".join(gram)] += 1

    return Counter({k: v for k,v in counter.items() if v >= min_freq})

def extract_terms(df: pd.DataFrame, glossary_df: pd.DataFrame, min_freq: int = 5) -> pd.DataFrame:
    ngram_freq = get_ngram_frequencies(df, min_freq=min_freq)
    term_data = []

    glossary_set = set(term.lower() for term in glossary_df["EN"])

    it_translations = defaultdict(list)

    for idx, row in df.iterrows():
        en = preprocess_text(row["EN"])
        it = row["Italian"]
        for n in range(1, 6):
            for gram in ngrams(en, n):
                phrase = " ".join(gram)
                if phrase in ngram_freq:
                    it_translations[phrase].append(it)

    for term_en, freq in ngram_freq.items():
        translations = it_translations[term_en]
        if translations:
            italian = Counter(translations).most_common(1)[0][0]
        else:
            italian = ""

        term_data.append({
                             "Term (EN)": term_en,
                             "Term (Italian)": italian,
                             "Frequency": freq,
                             "In Glossary?": "Yes" if check_against_glossary(term_en, glossary_df) else "No",
                             "Notes": ""
                         })

    return pd.DataFrame(term_data).sort_values(by="Frequency", ascending=False)
