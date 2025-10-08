from transformers import pipeline

# Tải model summarization nhẹ, có thể thay bằng API GPT nếu muốn
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize(text: str) -> str:
    """Tóm tắt nội dung dài thành 1–2 câu tự nhiên"""
    if not text or len(text) < 50:
        return text
    try:
        result = summarizer(text, max_length=60, min_length=15, do_sample=False)
        return result[0]["summary_text"]
    except Exception:
        return text