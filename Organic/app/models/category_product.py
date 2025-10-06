from django.db import models
from decimal import Decimal
from .supplier_certification import Supplier, Certification


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name="products")
    name = models.CharField(max_length=200)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    certifications = models.ManyToManyField(Certification, related_name="products", blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    sale = models.BooleanField(default=False)
    discount_percentage = models.FloatField(default=0, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        if self.sale:
            if self.sale_price and self.sale_price > 0:
                return self.sale_price
            elif self.discount_percentage:
                return Decimal(self.price) * (1 - Decimal(self.discount_percentage) / 100)
        return self.price
    
    @property
    def type(self):
        return "product"
    


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"{self.product.name} - Image"
    
class Nutrition(models.Model):
    product = models.OneToOneField("Product", on_delete=models.CASCADE, related_name="nutrition")
    calories = models.IntegerField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    carbs = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    fiber = models.FloatField(null=True, blank=True)
    sugar = models.FloatField(null=True, blank=True)
    sodium = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Dinh dưỡng của {self.product.name}"