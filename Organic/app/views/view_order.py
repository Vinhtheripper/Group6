from .view_cart import get_or_create_cart
from django.shortcuts import render, get_object_or_404, redirect
from app.models import  Order, OrderItem, ShippingAddress,Payment, Customer, Coupon
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib import messages
from decimal import Decimal
from .view_utils import applycoupon



#@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, "Your shopping cart is empty.")
        return redirect("cart")

    discount = Decimal(0)
    coupon_code = ""
    total = Decimal(cart.total)
    coupon_code = request.session.get("coupon_code", "")
    discount = Decimal(request.session.get("discount_amount", 0))
    total = Decimal(cart.total) - discount



    customer = getattr(request.user, "customer", None) if request.user.is_authenticated else None
    full_name = customer.name if customer else ""
    email = request.user.email if request.user.is_authenticated else ""
    phone = customer.phone if customer and customer.phone else ""

    if request.method == "POST":
        if "applycoupon" in request.POST:
            coupon_code = request.POST.get("coupon", "").strip()
            discount, error = applycoupon(cart, coupon_code)
            if error:
                messages.warning(request, error)
                discount = Decimal(0)
            else:
                messages.success(request, f"Apply {coupon_code} Successfull! Discount ${discount:,.0f}.")
                request.session["coupon_code"] = coupon_code
                request.session["discount_amount"] = float(discount)
            return redirect("checkout")

        
        elif "placeorder" in request.POST:
            full_name = request.POST.get("full_name", "").strip()
            phone = request.POST.get("phone", "").strip()
            address = request.POST.get("address", "").strip()
            payment_method = request.POST.get("payment", "cash")

           
            coupon_code = request.session.get("coupon_code", "")
            discount = Decimal(request.session.get("discount_amount", 0))
            total = Decimal(cart.total) - discount

            
            if not customer:
                customer = Customer.objects.create(name=full_name or "Guest", phone=phone)

            
            order = Order.objects.create(
                customer=customer,
                complete=False,
                payment_method=payment_method,
                status=Order.Status.PROCESSING,
            )

            
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code)
                    order.coupon = coupon
                    coupon.used_count += 1
                    if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
                        coupon.active = False
                    coupon.save(update_fields=["used_count", "active"])
                    order.save(update_fields=["coupon"])
                except Coupon.DoesNotExist:
                    pass

            # Địa chỉ giao hàng
            ShippingAddress.objects.create(
                order=order,
                customer=customer,
                address=address,
                city="",
                state="",
                mobile=phone,
            )

            for item in cart.items.all():
                if item.product:
                    price = getattr(item.product, "final_price", None) or item.product.price
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=price
                    )
                elif item.combo:
                    price = getattr(item.combo, "final_price", None) or item.combo.price
                    OrderItem.objects.create(
                        order=order,
                        combo=item.combo,
                        quantity=item.quantity,
                        price=price
                    )


            # Thanh toán
            Payment.objects.create(
                order=order,
                amount=total,
                transaction_id=get_random_string(12),
                status=Payment.Status.PENDING,
            )

            # Xóa giỏ hàng và session
            cart.items.all().delete()
            for key in ["coupon_code", "discount_amount"]:
                request.session.pop(key, None)

            messages.success(request, f"Order successful! Discount ${discount:,.0f}.")
            return redirect("success", order_id=order.id)
        
    return render(request, "app/checkout.html", {
        "cart": cart,
        "discount": discount,
        "total_after_discount": total,
        "coupon_code": coupon_code,
        "full_name": full_name,
        "email": email,
        "phone": phone,
    })


@login_required
def orderdetail(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id, customer__user=request.user)
    else:
        order = get_object_or_404(Order, id=order_id)
    
    status_map = {
    "placed":     ["done", "", "", ""],
    "processing": ["done", "done", "", ""],
    "confirmed":  ["done", "done", "done", ""],
    "shipping":   ["done", "done", "done", "shipping"],  # thêm bước đang giao
    "completed":  ["done", "done", "done", "done"],
    "canceled":   ["canceled", "", "", ""],  # toàn bộ reset, chỉ hiển thị hủy
        }

    s1, s2, s3, s4 = status_map.get(order.status, ["", "", "", ""])
    
    return render(request, "app/orderdetail.html", {
        "order": order,
        "s1": s1, "s2": s2, "s3": s3, "s4": s4
    })

def success(request, order_id):
    try:
        if request.user.is_authenticated:
            order = get_object_or_404(Order, id=order_id, customer__user=request.user)
        else:
            order = get_object_or_404(Order, id=order_id)
    except Order.DoesNotExist:
        order = None

    return render(request, "app/success.html", {"order": order})
