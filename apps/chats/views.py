from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import Http404
from .models import *
from .forms import *

@xframe_options_exempt
@login_required
def chat_view(request, chatroom_name="public-chat"):

    if chatroom_name == "public-chat":
        chat_group = ChatGroup.objects.filter(
            members=request.user, is_private=True
        ).first()
    else:
        chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)

    if not chat_group:
        # 조건에 맞는 chat_group이 없을 경우 기본 페이지 렌더링
        return render(
            request,
            "chats/chat.html",
            {
                "chat_messages": [],
                "form": ChatMessageCreateForm(),
                "other_user": None,
                "chatroom_name": chatroom_name,
                "other_user_is_online": False,
            },
        )

    chat_messages = chat_group.chat_messages.all()[:30]

    form = ChatMessageCreateForm(request.POST or None)

    other_user = None
    other_user_is_online = False
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                if other_user in chat_group.users_online.all():
                    other_user_is_online = True
                break

    if request.htmx:
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()

            context = {"message": message, "user": request.user}

            return render(request, "chats/partials/chat_message_p.html", context)

    context = {
        "chat_messages": chat_messages,
        "form": form,
        "other_user": other_user,
        "chatroom_name": chatroom_name,
        "other_user_is_online": other_user_is_online,
        "chat_group": chat_group,
    }

    return render(request, "chats/chat.html", context)


@xframe_options_exempt
@login_required
def start_chat_view(request, user_id):
    if request.user.id == user_id:
        return redirect("home")

    other_user = User.objects.get(id=user_id)
    my_private_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_private_chatrooms.exists():
        for chatroom in my_private_chatrooms:
            if other_user in chatroom.members.all():
                return redirect("chats:chatroom", chatroom.group_name)
    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)

    return redirect("chats:chatroom", chatroom.group_name)
