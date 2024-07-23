from django.urls import path
from .views import *

app_name = "profiles"
urlpatterns = [
    path("profile/", profile_view, name="profile"),
    path("profile/<str:username>/", profile_view, name="user_profile"),
]
