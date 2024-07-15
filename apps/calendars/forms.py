from django import forms
from .models import *
from .widgets import *


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            "title",
            "label",
            "start_date",
            "end_date",
            "all_day",
            "event_url",
            "location",
            "description",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "id": "eventTitle",
                    "name": "eventTitle",
                    "placeholder": "이벤트 제목",
                }
            ),
            "label": CustomSelect(
                attrs={
                    "class": "select2 select-event-label form-select",
                    "id": "eventLabel",
                    "name": "eventLabel",
                }
            ),
            "start_date": forms.DateTimeInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "id": "eventStartDate",
                    "name": "eventStartDate",
                    "placeholder": "시작일 선택",
                }
            ),
            "end_date": forms.DateTimeInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "id": "eventEndDate",
                    "name": "eventEndDate",
                    "placeholder": "종료일 선택",
                }
            ),
            "all_day": forms.CheckboxInput(
                attrs={
                    "type": "checkbox",
                    "class": "form-check-input allDay-switch",
                    "id": "allDaySwitch",
                }
            ),
            "event_url": forms.URLInput(
                attrs={
                    "type": "url",
                    "class": "form-control",
                    "id": "eventURL",
                    "name": "eventURL",
                    "placeholder": "https://www.coldpay.net",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "id": "eventLocation",
                    "name": "eventLocation",
                    "placeholder": "위치 입력",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "name": "eventDescription",
                    "id": "eventDescription",
                    "placeholder": "이벤트 설명",
                    "rows": 3,
                }
            ),
        }
