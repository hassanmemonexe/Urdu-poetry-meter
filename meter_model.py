# meter_model.py
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification

MODEL_PATH = "optimized_meter_model.pt"
MODEL_NAME = "bert-base-multilingual-cased"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model architecture
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME, num_labels=2)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device), strict=False)
model.to(device)
model.eval()

# Map prediction to ⏑ / –
label_map = {0: "⏑", 1: "–"}


def predict_meter_line(line: str) -> str:
    """
    Predict meter pattern for a single line
    """
    if not line.strip():
        return ""

    encoding = tokenizer(line, return_tensors='pt', truncation=True, padding=True).to(device)
    with torch.no_grad():
        outputs = model(**encoding)
    predictions = torch.argmax(outputs.logits, dim=-1)[0].cpu().numpy()

    # Map to ⏑ / –
    meter_seq = [label_map[p] for p in predictions[1:-1]]  # skip [CLS]/[SEP]

    # Optional smoothing: remove 5+ consecutive –
    smoothed = []
    count_dash = 0
    for m in meter_seq:
        if m == "–":
            count_dash += 1
        else:
            count_dash = 0
        if count_dash > 4:
            smoothed.append("⏑")
        else:
            smoothed.append(m)

    return "".join(smoothed)


def predict_meter_lines(lines: list) -> list:
    """
    Predict meter pattern for multiple lines separately
    """
    return [predict_meter_line(line) for line in lines if line.strip()]

