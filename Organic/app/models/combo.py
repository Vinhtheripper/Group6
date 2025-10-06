
from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from .category_product import Product



class Combo(models.Model):
    name = models.CharField(max_length=200)
    products = models.ManyToManyField("Product", through="ComboItem")
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="combos/", null=True, blank=True)
    discount_percentage = models.FloatField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # giá gốc tổng hợp
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def original_price(self):
        total = sum(item.product.price * item.quantity for item in self.comboitem_set.all())
        return Decimal(total).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def final_price(self):
        total = self.original_price
        discount = (total * Decimal(self.discount_percentage)) / 100
        return (total - discount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    @property
    def type(self):
        return "combo"

class ComboItem(models.Model):
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.combo.name} - {self.product.name} x{self.quantity}"