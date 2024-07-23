from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


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
    
    context = {
        'user': user,
        'profile': profile,
        'is_own_profile': user == request.user
    }
    return render(request, "profiles/profile.html", context)