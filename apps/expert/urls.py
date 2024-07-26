from django.urls import path
from .views import convert_to_expert

app_name = "experts"
urlpatterns = [
    path("experts/apply/", convert_to_expert, name="convert_to_expert"),
]
