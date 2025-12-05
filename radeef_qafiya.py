# radeef_qafiya.py

# Clean text helper
def clean_text(text):
    return text.strip()  # Add more normalization if needed

def detect_radeef_multi(lines):
    tokens = [clean_text(l).split() for l in lines if l.strip()]
    if not tokens or any(len(t) == 0 for t in tokens):
        return "Not found"

    radeef = []
    i = 1
    while True:
        try:
            last_words = [t[-i] for t in tokens]
        except IndexError:
            break
        if len(set(last_words)) == 1:
            radeef.insert(0, last_words[0])
            i += 1
        else:
            break
    return " ".join(radeef) if radeef else "Not found"

def detect_qafiya_multi(lines, radeef):
    qafiyas = []
    for line in lines:
        words = clean_text(line).split()
        if not words:
            qafiyas.append("Not found")
            continue
        if radeef != "Not found":
            r_words = radeef.split()
            if len(words) > len(r_words):
                q_word = words[-len(r_words)-1]
            else:
                q_word = words[-1]
        else:
            q_word = words[-1]
        qafiyas.append(q_word if q_word else "Not found")

    unique_qafiyas = list(set(qafiyas))
    return unique_qafiyas if unique_qafiyas else ["Not found"]
