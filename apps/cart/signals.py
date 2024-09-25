from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Cart
from django.db import transaction
import random

def generate_unique_qr_code():
    # generate random code with CART as prefix
    return "CART" + ''.join(random.choices("0123456789", k=6))

@receiver(pre_save, sender=Cart)
def set_qr_code(sender, instance, *args, **kwargs):
    """Set QR code before saving the Cart, if not already set."""
    if not instance.qr_code:  # If QR code is not set
        instance.qr_code = generate_unique_qr_code()
