
from django.db import models
from decimal import Decimal
from django.utils import timezone


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    discount_type = models.CharField(
        max_length=10,
        choices=[("percent", "Percent"), ("fixed", "Fixed Amount")],
        default="percent"
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    usage_limit = models.IntegerField(null=True, blank=True)
    used_count = models.IntegerField(default=0)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.discount_type} {self.discount_value})"

    def is_valid(self):
        now = timezone.now()
        return (
            self.active
            and (self.valid_from <= now <= (self.valid_to or now))
            and (self.usage_limit is None or self.used_count < self.usage_limit)
        )