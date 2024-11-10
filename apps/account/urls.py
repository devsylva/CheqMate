from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate_view, name='activate'),
    path('email-verification/', views.email_verification_view, name='email_verification'),
    path('email-verification-success/', views.email_verification_success_view, name='email_verification_success'),
    path("profile/", views.view_profile, name="view_profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]