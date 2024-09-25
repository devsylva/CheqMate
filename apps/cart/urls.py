from django.urls import path
from . import views

urlpatterns = [
    path("startshopping/", views.StartShoppingView.as_view(), name="startshopping"),
]