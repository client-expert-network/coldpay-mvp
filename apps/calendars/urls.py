from django.urls import path
from .views import *

app_name = "calendars"
urlpatterns = [
    path("calendar/", calendar_view, name="calendar"),
    # path("calendar/events/", event_list, name="event-list"),
    # path("calendar/events/create/", event_create, name="event-create"),
    # path("calendar/events/<id>/update/", event_update, name="event-update"),
    # path("calendar/events/<id>/delete/", event_delete, name="event-delete"),
    # path("events/", event_list_create, name="event_list_create"),  # 이벤트 목록 및 생성
    # path("events/<int:id>/", event_detail, name="event_detail"),
]
