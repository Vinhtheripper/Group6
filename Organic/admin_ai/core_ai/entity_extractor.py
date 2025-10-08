# app/ai/entity_extractor.py
import re
from datetime import datetime
from app.models import Customer, Product, Combo


def clean_name(text: str):
    """Làm sạch chuỗi và loại bỏ các từ thừa."""
    stopwords = ["nào", "gì", "này", "ấy", "đó", "hôm nay", "trong", "tháng", "năm"]
    for sw in stopwords:
        text = re.sub(rf"\b{sw}\b", "", text)
    return text.strip().title()


def extract_entities(message: str):
    """
    Trích xuất các thực thể (month, year, customer, product, combo, order_id)
    và hỗ trợ tiếng Việt tự nhiên hơn.
    """
    entities = {}
    msg = message.lower()

    #  Tháng
    if match := re.search(r"tháng\s*(\d{1,2})", msg):
        entities["month"] = int(match.group(1))

    #  Năm
    if match := re.search(r"năm\s*(\d{4})", msg):
        entities["year"] = int(match.group(1))

    now = datetime.now()
    entities.setdefault("month", now.month)
    entities.setdefault("year", now.year)

    #  Khách hàng — bắt "khách hàng [tên]" hoặc "[tên] có bao nhiêu đơn hàng"
    if match := re.search(r"khách hàng\s+([a-zA-ZÀ-ỹ\s]+)", msg):
        name = clean_name(match.group(1))
        match_cust = Customer.objects.filter(name__icontains=name).first()
        if match_cust:
            entities["customer"] = match_cust

    #  Sản phẩm — nhận “sản phẩm táo hữu cơ”, “mặt hàng gạo lứt”
    if match := re.search(r"(?:sản phẩm|mặt hàng|hàng hóa)\s+([a-zA-ZÀ-ỹ\s]+?)(?:$|,|\.|\?|!|\s+(giá|bán|nào|có|hữu cơ))", msg):
        name = clean_name(match.group(1))
        match_prod = Product.objects.filter(name__icontains=name).first()
        if match_prod:
            entities["product"] = match_prod

    #  Combo — “combo EatClean”, “combo giảm cân”, “combo Eat Clean”
    if match := re.search(r"combo\s+([a-zA-ZÀ-ỹ\s]+?)(?:$|,|\.|\?|!|\s+(mới|gồm|trong|có))", msg):
        name = clean_name(match.group(1))
        match_combo = Combo.objects.filter(name__icontains=name).first()
        if match_combo:
            entities["combo"] = match_combo

    #  Đơn hàng — hỗ trợ cả “đơn hàng số 15” hoặc “order 15”
    if match := re.search(r"(?:đơn hàng|order)(?:\s*số)?\s*(\d+)", msg):
        entities["order_id"] = int(match.group(1))

    return entities
