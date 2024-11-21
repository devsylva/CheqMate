from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.cart.models import Cart, CartItem


# Create your views here.
@login_required(login_url="login")
def checkoutSuccess(request):
    cartId = request.GET.get("reference")


    try:
        cart = Cart.objects.get(qr_code=cartId)  # Retrieve the cart instance
        cart.checked_out = True  # Mark the cart as checked out
        cart.save()

        with transaction.atomic():  # Use atomic transactions to ensure data consistency
            # Get all the CartItems related to this cart
            cart_items = cart.items.all()

            # Update the is_paid field for the associated products
            for cart_item in cart_items:
                product = cart_item.product
                product.is_paid = True
                product.save()


    except Cart.DoesNotExist:
        print(f"Cart with ID {cart_id} does not exist.")

    return render(request, "checkout/payment-success.html")

@login_required(login_url="login")
def checkoutCancelled(request):
    return render(request, "checkout/payment-cancelled.html")

@csrf_exempt
def flutterwaveWebhook(request):
    if request.method == "POST":
        secret_hash =  settings.FLUTTERWAVE_WEBHOOK_HASH
        signature = request.headers.get("verif-hash")
        if signature == None or (signature != secret_hash):
            # This request isn't from Flutterwave; discard
            return HttpResponse(status=401)

        # Retrieve the raw JSON data from the request
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        event_type = payload.get("event")
        
        if event_type == "charge.completed":
            pass
            # transaction_ref = payload["data"]["tx_ref"]
            # # Query your database to find the user associated with this transaction
            # # try:
            # payment = Payment.objects.get(transaction_ref=transaction_ref)
            # if payment.confirmed == True:
            #     return JsonResponse({"status": "Webhook received"}, status=200)
                
            # else:   
            #     payment.confirmed = True
            #     payment.save()
                
            #     user = payment.user
            #     # Update the user's balance
            #     payloadamount = payload["data"]["amount"]
            #     user.balance += Decimal(str(payloadamount))
            #     user.save()
            #     return JsonResponse({"status": "Webhook received"}, status=200)