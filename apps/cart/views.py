from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import Cart, Product, CartItem
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .utils import update_cart_sync_status
from decimal import Decimal
import qrcode
import os
import io

# Create your views here.

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html')


class StartShoppingView(APIView):
    def post(self, request):
        user = request.user

        cart = Cart.objects.filter(customer=user, checked_out=False).first()

        if not cart:
            cart = Cart.objects.create(customer=user)
        else:
            cart.items.all().delete()
        
        
        # Generate a unique filename for the QR code image
        qr_code_filename = f"qr_code_{get_random_string(6)}.png"
        qr_code_path = os.path.join(settings.MEDIA_ROOT, 'qrcodes', qr_code_filename)
        
        # Generate QR code with cart's qr_code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        ) 
        qr.add_data(str(cart.qr_code))
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")

        # Save image to the filesystem
        os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)  # Ensure the directory exists
        img.save(qr_code_path)

        # Return the URL to the generated QR code image
        qr_code_url = f"{settings.MEDIA_URL}qrcodes/{qr_code_filename}"

        return JsonResponse({
            'qrCodeURL': qr_code_url,  # Return the URL of the saved QR code
            'qrCode': cart.qr_code     # Return the cart's QR code (if needed for the WebSocket)
        })

# api endponit the cart sends a post request to when the user wants to sync a cart to a user
class SyncCartView(APIView):
    def post(self, request):
        qr_code = request.data.get('qr_code')

        try:
            # find the cart using the qr_cdoe and mark is as synced
            cart = Cart.objects.get(qr_code=qr_code)
            cart.is_synced = True
            cart.save()

            # Trigger the WebSocket update to notify the client
            update_cart_sync_status(qr_code, cart.is_synced)

            return JsonResponse({
                "success": True,
                "message": "Cart synced with user", 
                "cart_id": cart.id,
                "user_id": cart.customer.id
                }, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)


# api endpoint to check chart sync status
class SyncCartStatusView(APIView):
    def get(self, request):
        qr_code = request.GET.get('qr_code')
        
        
        cart = get_object_or_404(Cart, qr_code=qr_code)#Cart.objects.get(qr_code=qr_code)
        return JsonResponse({
            "success": True,
            "is_synced": cart.is_synced,
            "checked_out": cart.checked_out,
            "cart_id": cart.id,
            "user_id": cart.customer.id
        }, status=status.HTTP_200_OK)
        


# view cart page
def cart_view(request, qr_code):
    # Get the cart for the logged-in user where checkout is not yet completed
    cart = get_object_or_404(Cart, qr_code=qr_code, checked_out=False)

    # Get all items in the user's cart
    items = cart.items.all()
    for i in items:
        print(i.price)

    # Update the total price of the cart
    cart.update_total_price()


    # Calculate tax as a Decimal
    tax = cart.total_price * Decimal('0.1')
    total_price = cart.total_price + tax


    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
        'tax': tax,
        'sub_total': cart.total_price,
        'total_price': cart.total_price + tax,
        'futterwave_public_key': settings.FLUTTERWAVE_PUBLIC_KEY,
        'futterwave_encryption_key': settings.FLUTTERWAVE_ENCRYPTION_KEY,
        'futterwave_secret_key': settings.FLUTTERWAVE_SECRET_KEY,
    })


class AddToCartView(APIView):
    def post(self, request):
        cart_id = request.data.get('cart_id')
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, barcode=product_id)
        cart = get_object_or_404(Cart, qr_code=cart_id)

        cart_item = CartItem.objects.create(cart=cart, product=product, price=product.price)
        cart.update_total_price()

        return Response({"message": "Product added to cart", "cart_item_id": cart_item.id}, status=status.HTTP_200_OK)



class CartView(APIView):
    def get(self, request, qr_code):
        cart = get_object_or_404(Cart, qr_code=qr_code)
        cart_items = cart.cartitem_set.all()
        items = [{"product_id": item.product.id, "name": item.product.name, "price": item.price, "is_paid": item.is_paid} for item in cart_items]
        return Response({"cart": items, "total_price": cart.total_price}, status=status.HTTP_200_OK)


class RemoveFromCartView(APIView):
    def post(self, request):
        cart_id = request.data.get('cart_id')
        product_id = request.data.get('product_id')

        cart = get_object_or_404(Cart, id=cart_id)
        product = get_object_or_404(Product, id=product_id)

        # Find the CartItem and delete it
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.delete()

        # Update the total price of the cart
        cart.update_total_price()

        return Response({"message": "Product removed from cart"}, status=status.HTTP_200_OK)