# app/ai/agents/cert_agent.py
from app.models import Certification, Product

def handle_cert_intent(intent: str):
    """Xử lý các câu hỏi về chứng nhận sản phẩm."""
    if intent == "cert_list":
        certs = Certification.objects.values_list("name", flat=True)
        return f"GreenNest hiện có các chứng nhận: {', '.join(certs)}." if certs else "Chưa có chứng nhận nào."
    
    if intent == "cert_detail":
        cert = Certification.objects.first()
        if cert:
            return f"Chứng nhận {cert.name} do {cert.organization or 'N/A'} cấp. {cert.description or ''}"
        return "Không có dữ liệu chứng nhận."
    
    if intent == "cert_products":
        products = Product.objects.filter(certifications__isnull=False).distinct()
        names = ", ".join([p.name for p in products])
        return f"Các sản phẩm có chứng nhận hữu cơ: {names}." if names else "Chưa có sản phẩm nào có chứng nhận."
    
    return "Mình chưa rõ bạn muốn hỏi về chứng nhận nào."
