from django.shortcuts import render
from .models import *


# Create your views here.
def profile_view(request):
    return render(request, "profiles/profile.html")
