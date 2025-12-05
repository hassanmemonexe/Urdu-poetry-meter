# rhyme_suggestions.py
import re
import json
import numpy as np
from sentence_transformers import SentenceTransformer, util
from radeef_qafiya import detect_radeef_multi, detect_qafiya_multi

# ------------------ Text Cleaning ------------------ #
def clean_text(t):
    t = re.sub(r"[،۔!?؛]", "", t)
    return t.strip()

# ------------------ Phoneme Map ------------------ #
PH_MAP = {
    "ا": "A", "ہ": "A", "ء": "A", "آ": "A",
    "ی": "Y", "ے": "Y", "ئ": "Y",
    "و": "W",
    "ر": "R", "ڑ": "R",
    "ن": "N", "ں": "N",
    "م": "M",
    "ل": "L",
    "ک": "K", "ق": "K",
    "گ": "G", "غ": "G",
    "ت": "T", "ط": "T",
    "س": "S", "ث": "S", "ص": "S",
    "ز": "Z", "ذ": "Z", "ظ": "Z",
    "د": "D", "ڈ": "D", "ض": "D",
    "ب": "B", "پ": "B",
    "ف": "F"
}

def phoneme_tail(word):
    word = word.strip()
    tail = ""
    for ch in word[-3:]:
        tail += PH_MAP.get(ch, ch)
    return tail

# ------------------ Load Dataset for Suggestions ------------------ #
def load_dataset(json_path="qafiya_merged.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    qafiya_dict = {}
    for obj in data:
        q = obj["qafiya"].strip()
        qafiya_dict[q] = obj["words"]
    dataset_lines = []
    for words in qafiya_dict.values():
        dataset_lines.extend(words)
    return qafiya_dict, dataset_lines

qafiya_dict, dataset_lines = load_dataset()

# ------------------ Sentence Transformer Model ------------------ #
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# ------------------ Rhyme Suggestion Function ------------------ #
def suggest_rhymes(user_lines, top_k=10):
    user_lines = [clean_text(x) for x in user_lines]

    # 1) Radeef
    radeef = detect_radeef_multi(user_lines)

    # 2) Qafiya List
    qafiya_list = detect_qafiya_multi(user_lines, radeef)

    # 3) Phonetic Tail (from first Qafiya)
    phonetic_tail_val = phoneme_tail(qafiya_list[0]) if qafiya_list else ""

    # 4) Semantic Similarity
    user_embed = model.encode(" ".join(user_lines), convert_to_tensor=True)
    ds_embed = model.encode(dataset_lines, convert_to_tensor=True)
    sem_scores = util.cos_sim(user_embed, ds_embed)[0].cpu().numpy()

    # 5) Phoneme Matching Score
    ph_scores = []
    for line in dataset_lines:
        last_word = clean_text(line).split()[-1] if line.strip() else ""
        score = 1 if phoneme_tail(last_word).endswith(phonetic_tail_val) else 0
        ph_scores.append(score)
    ph_scores = np.array(ph_scores)

    # 6) Combined Score (weighted)
    final_score = 0.6 * sem_scores + 0.4 * ph_scores
    idx = np.argsort(final_score)[::-1][:top_k]

    suggestions = [{"sher": dataset_lines[i], "score": float(final_score[i])} for i in idx]

    return {
        "radeef": radeef,
        "qafiya": qafiya_list,
        "phonetic_tail": phonetic_tail_val,
        "suggestions": suggestions
    }
