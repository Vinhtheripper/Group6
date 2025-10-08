# app/ai/signals_sync.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from sentence_transformers import SentenceTransformer
import chromadb
from django.conf import settings
from app.models import Product, CustomerMessage, Certification

encoder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=f"{settings.BASE_DIR}/chroma_db")
collection = client.get_or_create_collection("greennest_realtime")

@receiver(post_save, sender=Product)
def sync_product(sender, instance, **kwargs):
    text = f"Sản phẩm {instance.name}, giá {instance.price}₫. {instance.description or ''}"
    emb = encoder.encode([text])[0]
    collection.upsert(ids=[f"product-{instance.id}"], documents=[text], embeddings=[emb])
    print(f" Synced Product {instance.name} vào ChromaDB realtime.")

@receiver(post_save, sender=CustomerMessage)
def sync_feedback(sender, instance, **kwargs):
    name = instance.customer.name if instance.customer else "Ẩn danh"
    text = f"Phản hồi từ {name}: {instance.message}. Đánh giá {instance.rating}/5."
    emb = encoder.encode([text])[0]
    collection.upsert(ids=[f"feedback-{instance.id}"], documents=[text], embeddings=[emb])
    print(f" Synced Feedback #{instance.id}.")

@receiver(post_save, sender=Certification)
def sync_cert(sender, instance, **kwargs):
    text = f"Chứng nhận {instance.name} bởi {instance.organization or 'N/A'}. {instance.description or ''}"
    emb = encoder.encode([text])[0]
    collection.upsert(ids=[f"cert-{instance.id}"], documents=[text], embeddings=[emb])
    print(f" Synced Certification {instance.name}.")
