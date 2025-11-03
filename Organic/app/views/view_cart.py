from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.models import Product, Cart, CartItem, Combo


def cart(request):
    user_cart = get_or_create_cart(request)
    return render(request, "app/cart.html", {"cart": user_cart})



def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart




def add_to_cart(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)

    qty = int(request.POST.get("quantity", 1))

    
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += qty
    else:
        item.quantity = qty
    item.save()

   
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("cart")))

def add_combo_to_cart(request, combo_id):
    cart = get_or_create_cart(request)
    combo = get_object_or_404(Combo, id=combo_id)
    qty = int(request.POST.get("quantity", 1))

    item, created = CartItem.objects.get_or_create(cart=cart, combo=combo)
    if not created:
        item.quantity += qty
    else:
        item.quantity = qty
    item.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("combodetail", args=[combo.id])))

def update_quantity(request, item_id, action):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    if action == "increase":
        item.quantity += 1
    elif action == "decrease" and item.quantity > 1:
        item.quantity -= 1
    item.save()
    return redirect("cart")


def remove_item(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return HttpResponseRedirect(reverse("cart") + "#cart")


def clear_or_remove_selected(request):
    cart = get_or_create_cart(request)
    selected_ids = request.POST.getlist("selected_items")

    if selected_ids:
        # Nếu người dùng có chọn item → chỉ xoá các item đó
        CartItem.objects.filter(cart=cart, id__in=selected_ids).delete()
    else:
        # Nếu không chọn gì → xoá toàn bộ giỏ hàng
        cart.items.all().delete()

    return redirect("cart")
    