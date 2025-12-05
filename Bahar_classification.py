# bahr.py
from difflib import SequenceMatcher

# ------------------ Bahr Templates ------------------ #
BAHAR_TEMPLATES = {
    "Ramal": "– ⏑ – ⏑ – ⏑ ⏑ – – ⏑ – ⏑ ⏑ ⏑ ⏑ – – ⏑ ⏑ – ⏑ ⏑ ⏑",
    "Hazaj": "– ⏑ – ⏑ – ⏑ – ⏑ – ⏑ – ⏑",
    "Kamil": "– – ⏑ – – ⏑ – – ⏑ – – ⏑",
    "Rajaz": "⏑ – ⏑ – ⏑ – ⏑ – ⏑ –",
    "Wafir": "⏑ ⏑ – ⏑ ⏑ – ⏑ ⏑ –",
    "Khor": "– ⏑ – – ⏑ – – ⏑ – –",
    "Mutdarik": "– ⏑ – ⏑ ⏑ – – ⏑ ⏑ –",
    "Sarīʿ": "– ⏑ – ⏑ – ⏑ – ⏑ – ⏑",
    "Musaddas": "⏑ – ⏑ – ⏑ – ⏑ – ⏑ – ⏑ – ⏑ –",
    "Mutaqārib": "– ⏑ – ⏑ – ⏑ – ⏑ – ⏑ –",
    "Basit": "⏑ – ⏑ – ⏑ – ⏑ –",
    "Majzūz": "– ⏑ – ⏑ – – ⏑ – ⏑",
    "Munsarih": "– ⏑ – – ⏑ – – ⏑",
    "Mahzuf": "– ⏑ – ⏑ – ⏑",
    "Mamdud": "– ⏑ – ⏑ – ⏑ –",
    "Hālat": "⏑ ⏑ – ⏑ ⏑ – ⏑ ⏑ –",
    "Mutaqaṭṭiʿ": "⏑ – ⏑ ⏑ – ⏑ ⏑ –",
    "Raml": "– ⏑ – ⏑ – ⏑ – ⏑",
    "Khabab": "– ⏑ – ⏑ ⏑ – ⏑ –"
}

# Normalize templates
TEMPLATES_NORMAL = {name: "".join(p.split()) for name, p in BAHAR_TEMPLATES.items()}

def _align_template(pred: str, templ: str) -> str:
    repeat = (len(pred) // len(templ)) + 1
    templ_ext = (templ * repeat)[:len(pred)]
    return templ_ext

def detect_best_bahr(predicted: str, threshold=0.8) -> dict:
    p_norm = "".join(predicted.split())
    best_score = 0
    best_name = None

    for name, templ_norm in TEMPLATES_NORMAL.items():
        aligned_template = _align_template(p_norm, templ_norm)
        score = SequenceMatcher(a=p_norm, b=aligned_template).ratio()
        if score > best_score:
            best_score = score
            best_name = name

    if best_score >= 0.95:
        label = "exact"
    elif best_score >= threshold:
        label = f"~{int(best_score*100)}% match"
    else:
        label = "low match"

    return {
        "Bahar": best_name,
    }
