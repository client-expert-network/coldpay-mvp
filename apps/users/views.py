import random
import string
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import SignupForm, LoginForm
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

User = get_user_model()


def signup_view(request):

    form = SignupForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email.split("@")[0]
            user.set_password(form.cleaned_data["password"])
            user.save()

            user = authenticate(
                request, email=user.email, password=form.cleaned_data["password"]
            )
            if user is not None:
                login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
                return HttpResponse("회원가입이 완료되었습니다.")
            else:
                return HttpResponse("사용자 인증에 실패했습니다.")
        else:
            # 폼 에러 확인
            print(form.errors)

    context = {"form": form}

    return render(request, "users/signup.html", context=context)


import logging

logger = logging.getLogger(__name__)


def send_verification_email(request):
    email = request.GET.get("email", None)
    if email:
        try:
            verification_code = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=6)
            )
            cache.set(
                email, verification_code, timeout=600
            )  # Cache the code for 10 minutes

            email_title = "Your Coldpay Verification Code"
            message = f"Your verification code is {verification_code}"
            email_message = EmailMessage(email_title, message, to=[email])
            email_message.send()

            return JsonResponse({"status": "sent"})
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {e}")
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "No email provided"})


def verify_code(request):
    email = request.GET.get("email", None)
    code = request.GET.get("code", None)
    cached_code = cache.get(email)
    if cached_code and cached_code == code:
        return JsonResponse({"status": "verified"})
    return JsonResponse({"status": "invalid"})


# 로그인
def login_view(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get("next", "/")

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponse(
                    "로그인 실패"
                )  # You might want to render a template with an error message

    context = {
        "form": form,
    }

    return render(request, "users/login.html", context=context)


def check_user_exists(request):
    email = request.GET.get("email", None)
    if email:
        user_exists = User.objects.filter(email=email).exists()
        return JsonResponse({"exists": user_exists})
    return JsonResponse({"exists": False})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            print("USER: ", user.id, user.username)
            email_title = "Coldpay Password Reset"
            message = f"Please click the link below to reset your password: http://localhost:8000/accounts/reset-password/{urlsafe_base64_encode(force_bytes(user.id))}/"    
            email_message = EmailMessage(email_title, message, to=[email])
            email_message.send()
            message = "Check your email for a password reset link."    
        else:
            message = "No user with that email address exists."
        print(message)
        return render(request, 'users/forgot_password.html', {'message': message})
    else:
        return render(request, 'users/forgot_password.html')

def reset_password(request, uidb64):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            message = "Passwords do not match."
            return render(request, 'users/reset_password.html', {'uidb64': uidb64, 'message': message})
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and new_password:
            if user.date_joined is None:
                user.date_joined = now()
            user.password = make_password(new_password)
            user.save()
            message = "Password reset successful."
            return redirect('accounts:login')
        else:
            message = "Invalid user or password."
            return render(request, 'users/reset_password.html', {'uidb64': uidb64, 'message': message})
    else:    
        return render(request, 'users/reset_password.html', {'uidb64': uidb64})