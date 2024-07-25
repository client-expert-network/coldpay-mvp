from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from apps.portfolios.models import Portfolio
from apps.services.models import Service


@login_required
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

    context = {
        "profile_user": user,
        "profile": profile,
        "is_own_profile": user == request.user,
        "portfolios": portfolios,
        "services": services,
        "portfolio_count": portfolio_count,
        "service_count": service_count,
    }
    return render(request, "profiles/profile.html", context)
