
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Customer, Order
from app.models import ChangePasswordForm
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from .view_cart import get_or_create_cart

@login_required
def myaccount(request):
    view_mode = request.GET.get("view", "profile")
    customer = getattr(request.user, "customer", None)
    recent_orders = Order.objects.filter(customer=customer).order_by("-date_order")[:3]
    recent_order = Order.objects.filter(customer=customer).order_by("-date_order").first()
    cart = get_or_create_cart(request)

    return render(request, "app/myaccount.html", {
        "customer": customer,
        "recent_orders": recent_orders,
        "recent_order": recent_order,
        "active_tab": view_mode,
        "cart": cart,
    })


@login_required
def editaccount(request):
    user = request.user
    customer = getattr(user, "customer", None)

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.email = request.POST.get("email", "")
        user.save()

        if customer:
            customer.phone = request.POST.get("phone", "")
            if request.FILES.get("customer_image"):
                customer.customer_image = request.FILES["customer_image"]
            customer.save()


        return redirect("myaccount")  

    return redirect("myaccount")


def authpage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        # Nếu là đăng ký
        if 'username' in request.POST:
            # Lấy dữ liệu từ form
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # Kiểm tra trùng mật khẩu
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return render(request, "app/auth.html", {"active_form": "register"})

            # Kiểm tra trùng username hoặc email
            if User.objects.filter(username=username).exists():
                messages.error(request, "The username already exists.")
                return render(request, "app/auth.html", {"active_form": "register"})
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already in use.")
                return render(request, "app/auth.html", {"active_form": "register"})

            # Tạo user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )

            # Tạo Customer mapping với User
            full_name = f"{first_name} {last_name}".strip() or username
            Customer.objects.get_or_create(user=user, defaults={"name": full_name})

            messages.success(request, "Registration successful! Please log in.")
            return render(request, "app/auth.html", {"active_form": "login"})

        # Nếu là đăng nhập
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")
        username = None
        if '@' in identifier:
            try:
                user_obj = User.objects.get(email=identifier)
                username = user_obj.username
            except User.DoesNotExist:
                messages.error(request, "Email does not exist.")
                return render(request, "app/auth.html", {"active_form": "login"})
        else:
            username = identifier

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')

        messages.error(request, "Wrong account or password.")
        return render(request, "app/auth.html", {"active_form": "login"})

    # Mặc định hiển thị login
    return render(request, "app/auth.html", {"active_form": "login"})


@login_required
def logoutPage(request):
    logout(request)
    return redirect('home')

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('myaccount')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'myaccount.html', {'form': form})