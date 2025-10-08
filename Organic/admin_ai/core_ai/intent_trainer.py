# app/ai/intent_trainer.py
import os, json, pickle, re
from typing import List, Tuple
from django.conf import settings
import numpy as np
import pandas as pd
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

INTENT_JSON = os.path.join(settings.BASE_DIR, "admin_ai", "core_ai", "intent_patterns.json")
MODEL_PKL   = os.path.join(settings.BASE_DIR, "admin_ai", "core_ai", "intent_model.pkl")
VECT_WORD   = os.path.join(settings.BASE_DIR, "admin_ai", "core_ai", "intent_vect_word.pkl")
VECT_CHAR   = os.path.join(settings.BASE_DIR, "admin_ai", "core_ai", "intent_vect_char.pkl")

def _normalize(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s

def _load_patterns() -> List[Tuple[str, str]]:
    data = json.load(open(INTENT_JSON, "r", encoding="utf-8"))
    if isinstance(data, dict):
        rows = [(ex, intent) for intent, examples in data.items() for ex in examples]
    else:
        rows = [(ex, d["intent"]) for d in data for ex in d["examples"]]
    # chuẩn hoá
    rows = [(_normalize(t), y) for t, y in rows]
    return rows

def train_and_save():
    rows = _load_patterns()
    df = pd.DataFrame(rows, columns=["text", "intent"])
    if df.empty:
        raise RuntimeError("intent_patterns.json rỗng!")

    # 2 vectorizer: word & char → robust với lỗi chính tả/biến thể
    vect_word = TfidfVectorizer(analyzer="word", ngram_range=(1,2), min_df=1)
    vect_char = TfidfVectorizer(analyzer="char_wb", ngram_range=(3,5), min_df=1)

    Xw = vect_word.fit_transform(df["text"])
    Xc = vect_char.fit_transform(df["text"])
    X  = hstack([Xw, Xc], format="csr")
    y  = df["intent"].values

    # split để report nhanh (không nặng)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    clf = LogisticRegression(max_iter=1000, class_weight="balanced", n_jobs=None)
    clf.fit(Xtr, ytr)

    ypred = clf.predict(Xte)
    print(" Validation report:\n", classification_report(yte, ypred, digits=3))

    # Lưu model & vectorizers
    pickle.dump(clf, open(MODEL_PKL, "wb"))
    pickle.dump(vect_word, open(VECT_WORD, "wb"))
    pickle.dump(vect_char, open(VECT_CHAR, "wb"))
    print(" Saved:", MODEL_PKL, VECT_WORD, VECT_CHAR)

if __name__ == "__main__":
    train_and_save()
