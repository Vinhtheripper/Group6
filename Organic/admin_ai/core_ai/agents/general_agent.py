# app/ai/agents/general_agent.py
import chromadb
from sentence_transformers import SentenceTransformer
from django.conf import settings

encoder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=f"{settings.BASE_DIR}/chroma_db")
collection = client.get_or_create_collection("greennest_daily")

def handle_general_query(query: str):
    """Fallback agent — dùng RAG để tìm thông tin tổng hợp."""
    emb = encoder.encode([query])
    res = collection.query(query_texts=[query], n_results=3)
    if not res or not res.get("documents"):
        return "Mình chưa tìm thấy thông tin phù hợp trong dữ liệu hiện có."
    docs = res["documents"][0]
    summary = "• " + "\n• ".join(docs)
    return f"Dựa trên dữ liệu, đây là tóm tắt ngắn:\n{summary}"
