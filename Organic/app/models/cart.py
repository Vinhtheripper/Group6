from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.db.models import Sum



class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        total = sum(item.subtotal for item in self.items.all())
        return total or Decimal(0)

    @property
    def total(self):
        return self.subtotal

    @property
    def items_count(self):
        return self.items.aggregate(total=Sum("quantity"))["total"] or 0

    @property
    def distinct_items(self):
        return self.items.count()

    def __str__(self):
        return f"Cart {self.id} - {self.user.username if self.user else f'Guest ({self.session_key})'}"

class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True, blank=True)
    combo = models.ForeignKey("Combo", on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        if self.product:
            return f"{self.product.name} x {self.quantity}"
        elif self.combo:
            return f"Combo: {self.combo.name} x {self.quantity}"
        return "Item không xác định"

    @property
    def item_name(self):
        if self.combo:
            return f"Combo: {self.combo.name}"
        elif self.product:
            return self.product.name
        return "Không xác định"

    @property
    def item_price(self):
        if self.combo:
            return Decimal(self.combo.final_price)
        elif self.product:
            return Decimal(self.product.final_price)
        return Decimal(0)

    @property
    def subtotal(self):
        return self.item_price * Decimal(self.quantity)