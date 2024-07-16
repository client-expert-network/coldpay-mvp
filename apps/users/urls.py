from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = "accounts"
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
    path("accounts/verify-code/", verify_code, name="verify-code"),
    path("accounts/forgot-password/", forgot_password, name="forgot-password"),
    path("accounts/reset-password/<str:uidb64>/", reset_password, name="reset-password"),
] + [
    path("accounts/check-user-exists/", check_user_exists, name="check-user-exists"),
]
