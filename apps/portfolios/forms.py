from django import forms
from .models import Portfolio


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = [
            "title",
            "content",
            "price",
            "portfolio_start",
            "portfolio_end",
        ]
        widgets = {
            "portfolio_start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "portfolio_end": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }