from django.urls import path
from .views import ConfirmProductPaymentView

urlpatterns = [
    path('api/confirm-product-payment/<int:barcode>/', ConfirmProductPaymentView.as_view(), name='confirm_product_payment'),
]