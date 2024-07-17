from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    expert = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=30)
