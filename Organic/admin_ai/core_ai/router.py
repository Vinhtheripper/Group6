# app/ai/router.py
from admin_ai.core_ai.intent_classifier import detect_intent
from admin_ai.core_ai.entity_extractor import extract_entities
from admin_ai.core_ai.agents.business_agent import handle_business_intent
from admin_ai.core_ai.agents.product_agent import handle_product_intent
from admin_ai.core_ai.agents.cert_agent import handle_cert_intent
from admin_ai.core_ai.agents.feedback_agent import handle_feedback_intent
from admin_ai.core_ai.agents.general_agent import handle_general_query


def answer(user_text: str) -> str:
    # 1️ Xác định intent bằng ML
    intent = detect_intent(user_text)
    # 2️ Trích xuất thực thể (entity)
    entities = extract_entities(user_text)

    print(f"[Intent] {user_text} → {intent} | Entities: {entities}")

    # 3️ Điều hướng tới agent phù hợp
    # Doanh thu, đơn hàng, khách hàng
    if intent.startswith("revenue") or intent in ["order_count", "loyal_customer"]:
        return handle_business_intent(intent, entities)

    # Sản phẩm, combo, đánh giá
    if intent in ["top_selling", "highest_price", "unsold", 
                  "combo_new", "product_organic_count", "product_highest_rated"]:
        return handle_product_intent(intent, entities)

    # Chứng nhận
    if intent.startswith("cert"):
        return handle_cert_intent(intent)

    # Feedback
    if intent.startswith("feedback"):
        return handle_feedback_intent(intent)

    # Fallback sang RAG nếu không match
    return handle_general_query(user_text)
