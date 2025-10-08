# app/ai/agents/feedback_agent.py
from app.models import CustomerMessage

def handle_feedback_intent(intent: str):
    """Tóm tắt phản hồi và đánh giá của khách hàng."""
    if intent == "feedback_summary":
        feedbacks = CustomerMessage.objects.all()[:5]
        if not feedbacks:
            return "Chưa có phản hồi nào từ khách hàng."
        summary = []
        for f in feedbacks:
            name = f.customer.name if f.customer else "Ẩn danh"
            summary.append(f"• {name}: {f.message} ({f.rating}/5)")
        return "Dưới đây là phản hồi gần đây:\n" + "\n".join(summary)
    return "Mình chưa rõ bạn muốn xem phản hồi nào."
