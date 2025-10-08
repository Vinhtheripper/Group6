# app/ai/exporter.py
import pandas as pd
import os
from django.conf import settings
from app.models import (
    Product, Order, CustomerMessage, Certification,
    Customer, Supplier, MealPlan, WeightTracking, Combo
)
from django.db.models import F, Sum

EXPORT_DIR = os.path.join(settings.BASE_DIR, "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)


#  Sản phẩm
def export_product():
    data = []
    for p in Product.objects.select_related("supplier").prefetch_related("certifications").all():
        certs = ", ".join([c.name for c in p.certifications.all()])
        supplier = getattr(p.supplier, "name", "Chưa rõ")
        category = getattr(p.category, "name", "Không phân loại")
        desc = p.description or "Không có mô tả."
        data.append({
            "id": p.id,
            "text": f"Sản phẩm {p.name} thuộc danh mục {category}, do {supplier} cung cấp. "
                    f"Giá {p.price:,.0f}₫. {desc} Chứng nhận: {certs or 'không có'}."
        })
    pd.DataFrame(data).to_csv(os.path.join(EXPORT_DIR, "products.csv"), index=False, encoding="utf-8-sig")


#  Đơn hàng
def export_order():
    data = []
    for o in Order.objects.select_related("customer").all():
        cust = o.customer.name if o.customer else "Ẩn danh"
        total = (
            o.orderitem_set.aggregate(total=Sum(F("price") * F("quantity")))["total"]
            or 0
        )
        data.append({
            "id": o.id,
            "text": f"Đơn hàng {o.id} của khách hàng {cust}, tổng giá trị {total:,.0f}₫, "
                    f"trạng thái: {o.status}, ngày đặt: {o.date_order.date()}."
        })
    pd.DataFrame(data).to_csv(os.path.join(EXPORT_DIR, "orders.csv"), index=False, encoding="utf-8-sig")

#  Phản hồi
def export_feedback():
    data = []
    for f in CustomerMessage.objects.select_related("customer").all():
        cust = f.customer.name if f.customer else "Ẩn danh"
        data.append({
            "id": f.id,
            "text": f"Phản hồi từ {cust}: {f.message}. Đánh giá: {f.rating}/5."
        })
    pd.DataFrame(data).to_csv(os.path.join(EXPORT_DIR, "feedbacks.csv"), index=False, encoding="utf-8-sig")


#  Chứng nhận
def export_certification():
    data = []
    for c in Certification.objects.all():
        data.append({
            "id": c.id,
            "text": f"Chứng nhận {c.name} do {c.organization or 'N/A'} cấp. {c.description or ''}"
        })
    pd.DataFrame(data).to_csv(os.path.join(EXPORT_DIR, "certifications.csv"), index=False, encoding="utf-8-sig")


#  Khách hàng
def export_customer():
    data = []
    for c in Customer.objects.all():
        data.append({
            "id": c.id,
            "text": f"Khách hàng {c.name} (số điện thoại: {c.phone or 'N/A'}), "
                    f"đã có {c.order_set.count()} đơn hàng."
        })
    pd.DataFrame(data).to_csv(os.path.join(EXPORT_DIR, "customers.csv"), index=False, encoding="utf-8-sig")


#  Nhà cung cấp
def export_supplier():
    data = []
    for s in Supplier.objects.all():
        data.append({
            "id": s.id,
            "text": f"Nhà cung cấp {s.name}, địa chỉ {s.address or 'chưa rõ'}, "
                    f"liên hệ: {s.phone or 'N/A'}."
        })
    pd.DataFrame(data).to_csv(os.path.join(EXPORT_DIR, "suppliers.csv"), index=False, encoding="utf-8-sig")


#  Meal Plan & Cân nặng
def export_meal_and_weight():
    meal_data = [
        {"id": m.id, "text": f"Thực đơn ngày {m.date} cho khách {m.customer.name if m.customer else 'Ẩn danh'}: {m.description or ''}. Tổng calo: {m.calories or 'chưa rõ'}."}
        for m in MealPlan.objects.select_related("customer").all()
    ]
    weight_data = [
        {"id": w.id, "text": f"Cập nhật cân nặng ngày {w.date}: {w.weight} kg (BMI: {w.bmi})."}
        for w in WeightTracking.objects.all()
    ]
    pd.DataFrame(meal_data).to_csv(os.path.join(EXPORT_DIR, "mealplans.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame(weight_data).to_csv(os.path.join(EXPORT_DIR, "weight_tracking.csv"), index=False, encoding="utf-8-sig")


#  Combo sản phẩm
def export_combo():
    data = []
    for c in Combo.objects.prefetch_related("comboitem_set__product").all():
        items = ", ".join([i.product.name for i in c.comboitem_set.all()])
        data.append({
            "id": c.id,
            "text": f"Combo {c.name} gồm các sản phẩm: {items or 'Không có sản phẩm'}. Tổng giá {getattr(c, 'final_price', 0):,.0f}₫."
        })
    pd.DataFrame(data).to_csv(os.path.join(EXPORT_DIR, "combos.csv"), index=False, encoding="utf-8-sig")


#  Gọi tất cả
def export_all():
    export_product()
    export_order()
    export_feedback()
    export_certification()
    export_customer()
    export_supplier()
    export_meal_and_weight()
    export_combo()
    print(" Exported full GreenNest dataset to /exports")
