from django.shortcuts import render, get_object_or_404
from app.models import Product
from .view_cart import get_or_create_cart


def productdetail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    related_products = Product.objects.filter(
        category__in=product.category.all()
    ).exclude(id=product.id).distinct()[:4]

    return render(request, "app/productdetail.html", {
        "product": product,
        "related_products": related_products,
        "cart": cart
    })

