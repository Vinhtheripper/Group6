
from django.shortcuts import render, get_object_or_404
from app.models import Product


def productdetail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    related_products = Product.objects.filter(
        category__in=product.category.all()
    ).exclude(id=product.id).distinct()[:4]

    return render(request, "app/productdetail.html", {
        "product": product,
        "related_products": related_products
    })

