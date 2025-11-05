import json
from .view_product import Product
from .view_combo import Combo
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from app.models import Category
from app.models import Coupon
from decimal import Decimal
from .view_cart import get_or_create_cart






def productlist(request):
    categories = Category.objects.all().order_by("name")
    selected_category_id = request.GET.get("category")

    if selected_category_id:
        # Lọc theo category
        products = Product.objects.filter(category__id=selected_category_id).order_by('-created_at')
        selected_category = get_object_or_404(Category, id=selected_category_id)
    else:
        # Nếu không chọn category nào thì có thể chọn mặc định
        selected_category = None
        products = Product.objects.all().order_by('-created_at')  

    combos = Combo.objects.all()
    cart = get_or_create_cart(request)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, "app/productlist.html", {
        "categories": categories,
        "page_object": page_object,
        "combos": combos,
        "cart": cart,
        "selected_category": selected_category_id,
    })


def search(request):
    query = request.GET.get("q", "").strip()
    results = []
    cart = get_or_create_cart(request)

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
        "cart": cart,
    })

def applycoupon(cart, code):
    try:
        coupon = Coupon.objects.get(code=code.strip(), active=True)
        if not coupon.is_valid():
            return None, "The coupon code has expired or is invalid."

        if Decimal(cart.total) < coupon.min_order_value:
            return None, "The order value has not reached the minimum amount to apply this code."

        if coupon.discount_type == "percent":
            discount = Decimal(cart.total) * (coupon.discount_value / Decimal(100))
        elif coupon.discount_type == "fixed":
            discount = coupon.discount_value
        else:
            return None, "Invalid coupon code type."

        discount = min(discount, Decimal(cart.total))
        return discount, None

    except Coupon.DoesNotExist:
        return None, "No coupon code found."
    





