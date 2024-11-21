from django.urls import path
from . import views


urlpatterns = [
    path("api/flutterwave/webhook/", views.flutterwaveWebhook, name="flutterwavewebhook"),
    path("payment/success/", views.checkoutSuccess, name="paymentsuccess"),
    path("payment/cancelled/", views.checkoutCancelled, name="paymentcancelled"),
]