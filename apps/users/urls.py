from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

# app_name = "accounts"
urlpatterns = [
    path("accounts/signup/", signup_view, name="signup"),
    path("accounts/login/", login_view, name="login"),
    path(
        "accounts/logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"
    ),
    path(
        "accounts/send-verification-email/",
        send_verification_email,
        name="send-verification-email",
    ),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
] + [
    path("accounts/check-user-exists/", check_user_exists, name="check-user-exists"),
]
