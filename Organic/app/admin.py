from django.contrib import admin
from . import views
from .models import *

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Certification)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Combo)
admin.site.register(ComboItem)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Payment)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Coupon)


