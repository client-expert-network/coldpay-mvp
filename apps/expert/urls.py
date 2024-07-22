from django.urls import path
from . import views

urlpatterns = [
    path('approval/<str:apply_id>/', views.expert_approval, name='expert_approval'),
    path('approval/', views.admin_expert_applications, name='admin_expert_approval'),
]