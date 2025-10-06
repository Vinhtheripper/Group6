
from django.db import models
from .user_customer import Customer
from django.utils.timezone import now

class CustomerMessage(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class WeightTracking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="weight_logs")
    date = models.DateField(default=now)
    height = models.FloatField()
    weight = models.FloatField()
    bmi = models.FloatField()
    health_status = models.CharField(max_length=50, default="Not rated yet")
