# accounts/adapter.py 파일 생성
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .utils import generate_random_korean_nickname
from django.contrib.auth import get_user_model

User = get_user_model()


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        extra_data = sociallogin.account.extra_data

        while True:
            username = generate_random_korean_nickname()
            if not User.objects.filter(username=username).exists():
                user.username = username
                break

        user.first_name = extra_data.get("given_name")
        user.last_name = extra_data.get("family_name")
        user.profile_picture = extra_data.get("picture")
        user.save()
        return user
