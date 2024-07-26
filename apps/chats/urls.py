from django.urls import path
from .views import *

app_name = "chats"
urlpatterns = [
    path("chats/", chat_view, name="chat"),
    path("chats/<user_id>/", start_chat_view, name="start_chat"),
    path("chats/chat/<chatroom_name>", chat_view, name="chatroom"),
    path("chats/chat/<chatroom_name>/leave/", chat_view, name="chatroom_leave"),
]
