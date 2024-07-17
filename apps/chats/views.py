from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *


@login_required
def chats_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="gveMsKZQZQvihyu3kKLo4X")
    chat_messages = chat_group.chat_messages.all()[:30]
    context = {"chat_messages": chat_messages}

    return render(request, "chats/chat.html", context=context)
