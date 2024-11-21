from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("cart/<str:qr_code>/", views.cart_view, name="cart_view"),

    # API Endpoints
    path("api/startshopping/", views.StartShoppingView.as_view(), name="api_startshopping"),
    path("api/cart/sync/", views.SyncCartView.as_view(), name="api_sync_cart"),
    path("api/cart/sync-status/", views.SyncCartStatusView.as_view(), name="api_sync_cart_status"),
    path("api/cart/add-item/", views.AddToCartView.as_view(), name="api_add_item_to_cart"),
    path("cart/remove-item/", views.RemoveFromCartView.as_view(), name="api_remove_item_from_cart"),
    path("api/cart/<str:qr_code>/", views.CartView.as_view(), name="api_cart_view"),
]