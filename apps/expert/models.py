from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth import get_user_model

User = get_user_model()


class ApplyExpert(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="expert_portfolios/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to="expert_portfolios/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
