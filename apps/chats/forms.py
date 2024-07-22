from django import forms
from .models import *


class ChatMessageCreateForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ["body"]
        labels = {"body": ""}
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "class": "form-control message-input border-0 me-4 shadow-none",
                    "placeholder": "내용을 입력하세요...",
                }
            )
        }
