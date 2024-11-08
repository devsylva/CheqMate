from django.shortcuts import render
import qrcode
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import Cart
from django.contrib.auth.models import User

# Create your views here.


def dashboard_view(request):
    return render(request, 'dashboard.html')

class StartShoppingView(APIView):
    def post(self, request):
        user = User.objects.get(id=1)#request.user
        cart = Cart.objects.create(customer=user)

        # Generate QR code
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
        
        # Save image to a BytesIO object
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Return the image as an HTTP response
        return HttpResponse(buffer, content_type="image/png")


# api endponit the cart sends a post request to when the user wants to sync a cart to a user
class SyncCartView(APIView):
    def post(self, request):
        qr_code = request.data.get('qr_code')

        try:
            # find the cart using the qr_cdoe and mark is as synced
            cart = Cart.objects.get(qr_code=qr_code)
            cart.is_synced = True
            cart.save()
            return JsonResponse({
                "success": True,
                "message": "Cart synced with user", "cart_id": cart.id
                }, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)


# api endpoint to check chart sync status
class SyncCartStatusView(APIView):
    def get(self, request):
        qr_code = request.GET.get('qr_code')
        
        try:
            cart = Cart.objects.get(qr_code=qr_code)
            return JsonResponse({
                "success": True,
                "is_synced": cart.is_synced,
                "cart_id": cart.id
            }, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Cart not found"
            }, status=status.HTTP_404_NOT_FOUND)


# view cart page
def cart_view(request, qr_code):
    # Get the cart for the logged-in user where checkout is not yet completed
    cart = get_object_or_404(Cart, qr_code="CART103390", checked_out=False)

    # Get all items in the user's cart
    items = cart.items.all()
    print(items)

    # Update the total price of the cart
    cart.update_total_price()

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
        'total_price': cart.total_price
    })


class AddToCartView(APIView):
    def post(self, request):
        cart_id = request.data.get('cart_id')
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart = get_object_or_404(Cart, id=cart_id)

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