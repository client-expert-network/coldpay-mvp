import random
import string
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import SignupForm
from django.contrib.auth import get_user_model

User = get_user_model()

def signup_view(request):
    form = SignupForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return HttpResponse("생성 완료. 이메일을 확인하세요.")

    context = {
        "form": form,
    }

    return render(request, "users/signup.html", context=context)
import logging

logger = logging.getLogger(__name__)

def send_verification_email(request):
    email = request.GET.get('email', None)
    if email:
        try:
            verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            cache.set(email, verification_code, timeout=600)  # Cache the code for 10 minutes
            
            email_title = "Your Coldpay Verification Code"
            message = f"Your verification code is {verification_code}"
            email_message = EmailMessage(email_title, message, to=[email])
            email_message.send()
            
            return JsonResponse({'status': 'sent'})
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'No email provided'})


def verify_code(request):
    email = request.GET.get('email', None)
    code = request.GET.get('code', None)
    cached_code = cache.get(email)
    if cached_code and cached_code == code:
        return JsonResponse({'status': 'verified'})
    return JsonResponse({'status': 'invalid'})

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
                return HttpResponse("로그인 실패")  # You might want to render a template with an error message

    context = {
        "form": form,
    }

    return render(request, "users/login.html", context=context)