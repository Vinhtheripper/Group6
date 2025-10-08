# app/ai/intent_classifier.py
import os, json, pickle, re
from difflib import SequenceMatcher
from functools import lru_cache
from django.conf import settings
from scipy.sparse import hstack

MODEL_PKL = os.path.join(settings.BASE_DIR, "admin_ai", "core_ai", "intent_model.pkl")
VECT_WORD = os.path.join(settings.BASE_DIR, "admin_ai", "core_ai", "intent_vect_word.pkl")
VECT_CHAR = os.path.join(settings.BASE_DIR, "admin_ai", "core_ai", "intent_vect_char.pkl")
PATTERNS  = os.path.join(settings.BASE_DIR, "admin_ai", "core_ai", "intent_patterns.json")


def _norm(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s

@lru_cache(maxsize=1)
def _load_patterns_list():
    data = json.load(open(PATTERNS, "r", encoding="utf-8"))
    if isinstance(data, dict):
        return list(data.items())
    return [(d["intent"], d["examples"]) for d in data]

def _fuzzy_fallback(text: str) -> str:
    items = _load_patterns_list()
    text = _norm(text)
    best, best_score = "general", 0.0
    for intent, exs in items:
        for ex in exs:
            score = SequenceMatcher(None, _norm(ex), text).ratio()
            if score > best_score:
                best, best_score = intent, score
    return best if best_score >= 0.45 else "general"

@lru_cache(maxsize=1)
def _load_model():
    if os.path.exists(MODEL_PKL) and os.path.exists(VECT_WORD) and os.path.exists(VECT_CHAR):
        clf  = pickle.load(open(MODEL_PKL, "rb"))
        vw   = pickle.load(open(VECT_WORD, "rb"))
        vc   = pickle.load(open(VECT_CHAR, "rb"))
        return clf, vw, vc
    return None, None, None

def detect_intent(text: str) -> str:
    clf, vw, vc = _load_model()
    if clf is None:
        # chưa train → dùng fuzzy
        return _fuzzy_fallback(text)

    s = _norm(text)
    Xw = vw.transform([s])
    Xc = vc.transform([s])
    X  = hstack([Xw, Xc], format="csr")
    proba = clf.predict_proba(X)[0]
    pred  = clf.classes_[proba.argmax()]
    # Ngưỡng tin cậy — nếu thấp, rơi về general
    return pred if proba.max() >= 0.40 else "general"
