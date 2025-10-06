from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, Order, Customer, User
import secrets

@receiver(post_save, sender=Payment)
def update_order_status(sender, instance, **kwargs):
    order = instance.order
    if instance.status == Payment.Status.PAID and order.status == Order.Status.PROCESSING:
        order.status = Order.Status.CONFIRMED
        order.is_paid = True
        order.complete = True
        order.save()

@receiver(post_save, sender=User)
def create_or_update_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance, name=instance.username)
    else:
        customer = getattr(instance, 'customer', None)
        if customer:
            customer.name = f"{instance.first_name} {instance.last_name}".strip() or instance.username
            customer.save()


def _gen_ref_code():
    return secrets.token_urlsafe(6)[:12].upper()

@receiver(post_save, sender=Customer)
def ensure_referral_code(sender, instance, created, **kwargs):
    if created and not instance.referral_code:
        instance.referral_code = _gen_ref_code()
        instance.save(update_fields=["referral_code"])