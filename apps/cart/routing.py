from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/cart/<str:cart_id>/', consumers.CartConsumer.as_asgi()),
]