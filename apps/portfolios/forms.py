from django import forms
from .models import Portfolio
from tinymce.widgets import TinyMCE

class PortfolioForm(forms.ModelForm):   

    class Meta:
        model = Portfolio
        fields = [
            "title",
            "htmlcontent",
            "price",
            "portfolio_start",
            "portfolio_end",
        ]
        widgets = {
            "portfolio_start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "portfolio_end": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }