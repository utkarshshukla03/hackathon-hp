import re

ABBREVIATIONS = {
    "cs": "carbon steel",
    "ss": "stainless steel",
    "dia": "diameter",
    "od": "outer diameter",
    "id": "inner diameter"
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\.]", " ", text)

    for abbr, full in ABBREVIATIONS.items():
        text = re.sub(rf"\b{abbr}\b", full, text)

    text = re.sub(r"\s+", " ", text).strip()
    return text
