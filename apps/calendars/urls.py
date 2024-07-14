from django.urls import path
from .views import *

app_name = "calendars"
urlpatterns = [
    path("calendar/", calendar_view, name="calendar"),
]
