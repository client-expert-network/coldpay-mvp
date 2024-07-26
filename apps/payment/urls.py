from django.urls import path
from .views import *

app_name = "payment"
urlpatterns = [
    path("payment/", index, name="index"),
    path("cancel/", cancel_auth, name="cancel"),
    path("serverAuth/", server_auth, name="clientAuth"),
]

