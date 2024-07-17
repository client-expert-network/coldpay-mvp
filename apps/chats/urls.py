from django.urls import path
from .views import *

app_name = "chats"
urlpatterns = [
    path("chats/", chats_view, name="chats"),
]
