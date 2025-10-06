
from django.db import models
from decimal import Decimal
from .user_customer import Customer
from .category_product import Product
from .combo import Combo
class Order(models.Model):
    class Status(models.TextChoices):
        PLACED     = "placed",     "Đã đặt"
        PROCESSING = "processing", "Đang xử lý"
        CONFIRMED  = "confirmed",  "Đã xác nhận"
        SHIPPING   = "shipping",   "Đang vận chuyển"
        COMPLETED  = "completed",  "Hoàn tất"
        CANCELED   = "canceled",   "Đã hủy"

    PAYMENT_METHODS = [
        ("cash", "COD"),
        ("momo", "Momo"),
        ("vnpay", "VNPay"),
        ("bank", "Chuyển khoản"),
    ]

    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_order= models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, null=True, blank=True)
    complete = models.BooleanField(default=False)
    is_paid= models.BooleanField(default=False)
    used_reward= models.BooleanField(default=False)
    coupon= models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    status= models.CharField(max_length=20, choices=Status.choices, default=Status.PLACED)

    def __str__(self):
        return f"Order {self.id}"

    @property
    def get_cart_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())

    @property
    def get_cart_total(self):
        total = sum(item.get_total for item in self.orderitem_set.all())
        if self.used_reward:
            total *= Decimal("0.90")
        if self.coupon and self.coupon.is_valid():
            if self.coupon.discount_type == "percent":
                total *= (Decimal("1.0") - (self.coupon.discount_value / Decimal("100")))
            elif self.coupon.discount_type == "fixed":
                total -= self.coupon.discount_value
        return max(total, Decimal("0.00"))


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING  = "pending",  "Pending"
        PAID     = "paid",     "Paid"
        FAILED   = "failed",   "Failed"
        REFUNDED = "refunded", "Refunded"

    order= models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    amount= models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    status= models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    created_at= models.DateTimeField(auto_now_add=True)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    combo = models.ForeignKey(Combo, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def get_total(self):
        if self.combo:
            return self.combo.final_price * self.quantity
        elif self.product:
            return self.product.final_price * self.quantity
        return 0