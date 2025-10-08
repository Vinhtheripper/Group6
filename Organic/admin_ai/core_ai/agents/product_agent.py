from app.models import Product, Combo, OrderItem, CustomerMessage
from django.utils.timezone import now
from django.db.models import Count, Avg
from datetime import timedelta

def handle_product_intent(intent: str) -> str:
    """Xử lý các intent liên quan đến sản phẩm, combo, organic, đánh giá."""
    
    # 🥇 Bán chạy nhất
    if intent == "top_selling":
        top = (
            Product.objects.annotate(sales=Count("orderitem"))
            .order_by("-sales")
            .first()
        )
        if top:
            return f"Sản phẩm bán chạy nhất là {top.name} ({top.sales} lượt bán)."
        return "Chưa có dữ liệu bán hàng."

    # 💰 Sản phẩm đắt nhất
    if intent == "highest_price":
        p = Product.objects.order_by("-price").first()
        if p:
            return f"Sản phẩm có giá cao nhất là {p.name}, giá {p.price:,.0f}₫."
        return "Không tìm thấy sản phẩm."

    # 🚫 Sản phẩm chưa bán
    if intent == "unsold":
        unsold = Product.objects.filter(orderitem__isnull=True)
        if unsold.exists():
            names = ", ".join(p.name for p in unsold)
            return f"Các sản phẩm chưa từng bán: {names}."
        return "Tất cả sản phẩm đều đã có lượt bán."

    # 🧩 Combo mới trong tháng
    if intent == "combo_new":
        start_month = now().replace(day=1)
        new_combos = Combo.objects.filter(created_at__gte=start_month)
        if new_combos.exists():
            names = ", ".join(c.name for c in new_combos)
            return f"Tháng này có các combo mới: {names}."
        return "Chưa có combo nào mới trong tháng này."

    # 🌿 Đếm số sản phẩm hữu cơ (organic)
    if intent == "product_organic_count":
        organic = Product.objects.filter(certifications__name__icontains="hữu cơ").distinct().count()
        return f"Hiện có {organic} sản phẩm đạt chứng nhận hữu cơ."

    # ⭐ Sản phẩm được đánh giá cao nhất
    if intent == "product_highest_rated":
        rated = (
            CustomerMessage.objects.filter(rating__isnull=False)
            .aggregate(avg_rating=Avg("rating"))
        )
        if rated and rated["avg_rating"]:
            return f"Điểm đánh giá trung bình từ khách hàng là {rated['avg_rating']:.1f}/5."
        return "Chưa có dữ liệu đánh giá từ khách hàng."


    # fallback
    return "Tôi chưa rõ bạn đang hỏi về sản phẩm nào."
