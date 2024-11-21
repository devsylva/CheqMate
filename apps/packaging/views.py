from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from apps.cart.models import Product
from django.http import JsonResponse
from rest_framework import status


# Create your views here.
class ConfirmProductPaymentView(APIView):
    def get(self, request, barcode):
        product = get_object_or_404(Product, barcode=barcode)
        print(product)
        if product.is_paid == True:
            return JsonResponse({"message": "Product already paid for"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"message": "Product not yet paid for"}, status=status.HTTP_200_OK)

        