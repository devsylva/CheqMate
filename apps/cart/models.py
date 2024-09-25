from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    barcode = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    qr_code = models.CharField(max_length=20, unique=True, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart ({self.customer.username}) - Total: {self.total_price}"

    def update_total_price(self):
        self.total_price = sum(item.price for item in self.cartitem_set.all())
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} in {self.cart.customer.username}'s cart"