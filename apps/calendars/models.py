from django.db import models
from shortuuid.django_fields import ShortUUIDField

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Event(models.Model):
    LABEL_CHOICES = [
        ("업무", "업무"),
        ("개인", "개인"),
        ("가족", "가족"),
        ("휴일", "휴일"),
        ("기타", "기타"),
    ]

    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="제목")
    label = models.CharField(max_length=20, choices=LABEL_CHOICES, verbose_name="라벨")
    start_date = models.DateTimeField(verbose_name="시작일")
    end_date = models.DateTimeField(verbose_name="종료일", blank=True, null=True)
    all_day = models.BooleanField(default=False, verbose_name="종일")
    event_url = models.URLField(blank=True, null=True, verbose_name="이벤트 URL")
    location = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="위치"
    )
    description = models.TextField(blank=True, null=True, verbose_name="설명")

    def __str__(self):
        return self.title
