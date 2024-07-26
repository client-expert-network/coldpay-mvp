from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from apps.portfolios.models import Portfolio
from apps.services.models import Service
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.template.loader import render_to_string


def profile_view(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    try:
        profile = Profile.objects.get(expert=user)
    except Profile.DoesNotExist:
        profile = None

    portfolios = Portfolio.objects.filter(expert=user).order_by("-created_at")
    services = Service.objects.filter(seller=user).prefetch_related(
        "priceoption_set", "category_detail__category"
    )

    portfolio_count = portfolios.count()
    service_count = services.count()

    if request.user.is_authenticated:
        is_following = request.user.is_following(user) if request.user != user else None
    else:
        is_following = None

    follower_count = user.followers.count()
    following_count = user.following.count()

    context = {
        "profile_user": user,
        "profile": profile,
        "is_own_profile": user == request.user,
        "portfolios": portfolios,
        "services": services,
        "portfolio_count": portfolio_count,
        "service_count": service_count,
        "is_following": is_following,
        "follower_count": follower_count,
        "following_count": following_count,
    }
    return render(request, "profiles/profile.html", context)


@login_required
@require_POST
def follow_unfollow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user == user_to_follow:
        return JsonResponse(
            {"status": "error", "message": "자기 자신을 팔로우할 수 없습니다."}
        )

    if request.user.is_following(user_to_follow):
        request.user.unfollow(user_to_follow)
        is_following = False
    else:
        request.user.follow(user_to_follow)
        is_following = True

    context = {
        "profile_user": user_to_follow,
        "is_following": is_following,
        "user": request.user,
    }

    button_html = render_to_string(
        "profiles/follow_button.html", context, request=request
    )
    response = HttpResponse(button_html)
    response["HX-Trigger"] = "followToggled"
    return response


def follower_count(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return HttpResponse(str(user.followers.count()))


def following_count(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return HttpResponse(str(user.following.count()))
