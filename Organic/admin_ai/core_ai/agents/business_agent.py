# app/ai/agents/business_agent.py
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.utils.timezone import now
from app.models import Order, OrderItem

def handle_business_intent(intent: str, entities: dict = None):
    """
    Xử lý các intent liên quan đến doanh thu, đơn hàng, khách hàng cụ thể, hoặc theo tháng.
    """
    entities = entities or {}
    today = now().date()
    month = entities.get("month", today.month)
    year = entities.get("year", today.year)
    customer = entities.get("customer")

    # 🧾 Tổng doanh thu toàn hệ thống
    if intent == "revenue_total":
        total = (
            OrderItem.objects.aggregate(
                total=Sum(ExpressionWrapper(F("price") * F("quantity"), output_field=DecimalField()))
            )["total"]
            or 0
        )
        count = Order.objects.count()
        return f"Tổng doanh thu toàn hệ thống là {total:,.0f}₫ với {count} đơn hàng."

    # 📅 Doanh thu hôm nay
    if intent == "revenue_today":
        total = (
            OrderItem.objects.filter(order__date_order__date=today)
            .aggregate(total=Sum(F("price") * F("quantity")))["total"]
            or 0
        )
        return f"Doanh thu hôm nay là {total:,.0f}₫."

    # 🗓️ Doanh thu theo tháng/năm (từ entity)
    if intent == "revenue_month":
        total = (
            OrderItem.objects.filter(
                order__date_order__month=month,
                order__date_order__year=year
            )
            .aggregate(total=Sum(F("price") * F("quantity")))["total"]
            or 0
        )
        return f"Doanh thu tháng {month}/{year} là {total:,.0f}₫."

    # 👤 Số lượng đơn hàng của khách hàng cụ thể
    if intent == "order_count" and customer:
        count = Order.objects.filter(customer=customer).count()
        return f"Khách hàng {customer.name} có tổng cộng {count} đơn hàng."
    
    if intent == "revenue_compare":
        this_month = today.month
        last_month = this_month - 1 or 12
        this_total = (
            OrderItem.objects.filter(order__date_order__month=this_month)
            .aggregate(total=Sum(ExpressionWrapper(F("price") * F("quantity"), output_field=DecimalField())))
            .get("total") or 0
        )
        last_total = (
            OrderItem.objects.filter(order__date_order__month=last_month)
            .aggregate(total=Sum(ExpressionWrapper(F("price") * F("quantity"), output_field=DecimalField())))
            .get("total") or 0
        )

        diff = this_total - last_total
        if last_total == 0:
            growth = None
            trend_desc = "tăng vô hạn (vì tháng trước chưa có doanh thu)"
        else:
            growth = (diff / last_total * 100)
            trend_desc = f"{'tăng' if diff > 0 else 'giảm'} {abs(growth):.1f}% so với tháng trước."

        trend = "tăng" if diff > 0 else "giảm"
        if growth is None:
            return f"Doanh thu tháng này là {this_total:,.0f}₫, {trend_desc}."
        return f"Doanh thu tháng này là {this_total:,.0f}₫, {trend_desc}"


    if intent == "revenue_cancel_rate":
        total = OrderItem.objects.count()
        cancelled = OrderItem.objects.filter(order__status__iexact="cancelled").count()
        rate = (cancelled / total * 100) if total else 0
        return f"Tỉ lệ đơn hàng bị hủy là {rate:.1f}%."

    # 🔁 Mặc định nếu không rõ yêu cầu
    return "Mình chưa rõ bạn muốn xem báo cáo doanh thu nào."

    
