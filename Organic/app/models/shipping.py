
from django.db import models
from decimal import Decimal
from .user_customer import Customer
from .order_payment import Order


class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    state = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

class Delivery(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shipping", "Shipping"),
        ("delivered", "Delivered"),
        ("failed", "Failed"),
    ]

    order = models.OneToOneField("Order", on_delete=models.CASCADE, related_name="delivery")
    carrier = models.CharField(max_length=100, null=True, blank=True)  # tên đơn vị vận chuyển
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    estimated_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery for Order {self.order.id} - {self.status}"