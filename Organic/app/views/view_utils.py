import json
from .view_product import Product
from .view_combo import Combo
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from app.models import Coupon
from decimal import Decimal
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json





def productlist(request):
    products = Product.objects.all().order_by('-created_at')
    combos = Combo.objects.all()

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, "app/productlist.html", {
        "page_object": page_object,  
        "combos": combos,
    })


def search(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(certifications__name__icontains=query)
        ).order_by("-created_at").distinct()

    return render(request, "app/search.html", {
        "query": query,
        "results": results,
    })

def applycoupon(cart, code):
    try:
        coupon = Coupon.objects.get(code=code.strip(), active=True)
        if not coupon.is_valid():
            return None, "Mã giảm giá đã hết hạn hoặc không hợp lệ."

        if Decimal(cart.total) < coupon.min_order_value:
            return None, "Giá trị đơn hàng chưa đạt mức tối thiểu để áp dụng mã này."

        if coupon.discount_type == "percent":
            discount = Decimal(cart.total) * (coupon.discount_value / Decimal(100))
        elif coupon.discount_type == "fixed":
            discount = coupon.discount_value
        else:
            return None, "Loại mã giảm giá không hợp lệ."

        discount = min(discount, Decimal(cart.total))
        return discount, None

    except Coupon.DoesNotExist:
        return None, "Không tìm thấy mã giảm giá."
    





