from django.urls import path
from .views import *

app_name = "profiles"
urlpatterns = [
    path("profile/", profile_view, name="profile"),
    path("profile/<str:username>/", profile_view, name="user_profile"),
    path("follow/<str:user_id>/", follow_unfollow, name="follow_unfollow"),
    path("follower_count/<str:user_id>/", follower_count, name="follower_count"),
    path("following_count/<str:user_id>/", following_count, name="following_count"),
]
