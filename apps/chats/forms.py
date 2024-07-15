from django import forms
from .models import *


class ChatMessageCreateForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ["body"]


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ["groupchat_name"]


class ChatRoomEditForm(forms.ModelForm):

    class Meta:
        model = ChatGroup
        fields = ["groupchat_name"]
