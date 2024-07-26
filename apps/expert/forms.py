from django import forms
from .models import ApplyExpert


class ExpertConversionForm(forms.ModelForm):
    class Meta:
        model = ApplyExpert
        fields = ["title", "image", "video", "description"]
