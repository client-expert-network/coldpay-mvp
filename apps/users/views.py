from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import *
from .tokens import *

from django.contrib.auth import get_user_model
from .forms import *

User = get_user_model()


# 회원가입
def signup_view(request):
    form = SignupForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_email(request, user)
            return HttpResponse("생성 완료")

    context = {
        "form": form,
    }

    return render(request, "users/signup.html", context=context)


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
                # 로그인 실패 처리
                return HttpResponse("로그인 실패")

    context = {
        "form": form,
    }

    return render(request, "users/login.html", context=context)


# 인증 메일 발송 함수
def send_activation_email(request, user):

    email_title = "Coldpay - Activate Your Account!"
    activation_link = f"http://127.0.0.1:8000/accounts/user/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{account_activation_token.make_token(user)}/"

    message = render_to_string(
        "users/activation_email.html",
        {
            "user": user,
            "activation_link": activation_link,
        },
    )
    email = EmailMessage(email_title, message, to=[user.email])
    email.send()


# 유저 활성화 함수
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        message = "Thank you for confirming your email. Your account is now active."
        detail = "You can now log in using your credentials."
    else:
        message = "Activation link is invalid!"
        detail = "Please try registering again or contact support for assistance."

    return render(
        request, "users/activation_result.html", {"message": message, "detail": detail}
    )
