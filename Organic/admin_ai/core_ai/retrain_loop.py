import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from django.conf import settings

#  Load embedding model (nhẹ, nhanh)
encoder = SentenceTransformer("all-MiniLM-L6-v2")

#  Khởi tạo ChromaDB client
client = chromadb.PersistentClient(path=f"{settings.BASE_DIR}/chroma_db")
collection = client.get_or_create_collection("greennest_daily")


def rebuild_from_csv():
    """
    Huấn luyện lại toàn bộ Chroma index từ các file CSV trong /exports.
    Bỏ qua file rỗng hoặc sai định dạng.
    """
    base = os.path.join(settings.BASE_DIR, "exports")
    csv_files = [
        "products.csv", "orders.csv", "feedbacks.csv", "certifications.csv",
        "customers.csv", "suppliers.csv", "mealplans.csv", "weight_tracking.csv", "combos.csv"
    ]

    docs, ids = [], []

    for file in csv_files:
        path = os.path.join(base, file)
        if not os.path.exists(path):
            print(f" File not found: {file}")
            continue

        try:
            df = pd.read_csv(path)
        except Exception as e:
            print(f" Failed to read {file}: {e}")
            continue

        #  Bỏ qua file rỗng hoặc không có cột text
        if df.empty or "text" not in df.columns:
            print(f" Skipped empty or invalid file: {file}")
            continue

        for _, row in df.iterrows():
            text = str(row.get("text", "")).strip()
            if not text:
                continue
            docs.append(text)
            ids.append(f"{file.split('.')[0]}-{row.get('id', len(ids))}")

    if not docs:
        print(" No valid documents found in any CSV file.")
        return

    print(f" Tổng số dòng hợp lệ: {len(docs)} → Bắt đầu encode embeddings...")

    #  Encode tất cả văn bản
    emb = encoder.encode(docs)

    #  Xóa index cũ
    try:
        collection.delete(ids=[])  # clear toàn bộ collection
        print("🧹 Cleared old vector store.")
    except Exception as e:
        print(f" Could not clear collection: {e}")

    #  Thêm lại dữ liệu mới
    try:
        collection.add(documents=docs, embeddings=emb, ids=ids)
        print(f" Rebuilt Chroma index with {len(docs)} documents.")
    except Exception as e:
        print(f" Failed to add embeddings: {e}")
