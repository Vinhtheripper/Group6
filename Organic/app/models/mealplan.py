
from django.db import models
from .user_customer import Customer
from .category_product import Product
from .combo import Combo


class MealPlan(models.Model):
    WEEKDAYS = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="meal_plans")
    week = models.IntegerField(default=1)  
    day = models.CharField(max_length=10, choices=WEEKDAYS)
    breakfast = models.ManyToManyField(Product, related_name="mealplan_breakfast", blank=True)
    lunch = models.ManyToManyField(Product, related_name="mealplan_lunch", blank=True)
    dinner = models.ManyToManyField(Product, related_name="mealplan_dinner", blank=True)
    snacks = models.ManyToManyField(Product, related_name="mealplan_snacks", blank=True)
    combos = models.ManyToManyField(Combo, related_name="mealplan_combos", blank=True)

    class Meta:
        unique_together = ("customer", "week", "day")

    def __str__(self):
        return f"{self.customer} - Week {self.week} - {self.day}"