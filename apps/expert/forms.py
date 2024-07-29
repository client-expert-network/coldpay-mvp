from django import forms
from .models import ApplyExpert


class ExpertConversionForm(forms.ModelForm):
    class Meta:
        model = ApplyExpert
        fields = ["title", "image", "video", "description"]
        labels = {
            "title": "제목",
            "image": "이미지",
            "video": "비디오",
            "description": "설명",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "", "class": "form-control"}
            ),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "video": forms.FileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }
