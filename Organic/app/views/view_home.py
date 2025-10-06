from django.shortcuts import render
from django.utils import timezone
from app.models import Product, Coupon
from django.db.models import Q


def home(request):
    new_products = Product.objects.order_by('-created_at')[:4]
    now = timezone.now()
    valid_coupons = Coupon.objects.filter(
        active=True,
        valid_from__lte=now
    ).filter(
        Q(valid_to__gte=now) | Q(valid_to__isnull=True)
    ).order_by('-valid_from')

    current_coupon = None
    for c in valid_coupons:
        if (c.usage_limit is None) or (c.used_count < c.usage_limit):
            current_coupon = c
            break  
    return render(request, 'app/home.html', {'new_products': new_products, 'current_coupon': current_coupon})