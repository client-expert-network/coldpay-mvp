from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField

User = get_user_model()


class Portfolio(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    expert = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    htmlcontent = HTMLField(default="")   #HTMLField 추가
    price = models.IntegerField()
    portfolio_start = models.DateTimeField()
    portfolio_end = models.DateTimeField()
    show = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_duration(self):
        return self.portfolio_end - self.portfolio_start


class PortfolioImage(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    portfolio = models.ForeignKey(
        Portfolio, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="portfolio_images")


class PortfolioVideo(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    portfolio = models.ForeignKey(
        Portfolio, related_name="videos", on_delete=models.CASCADE
    )
    video = models.FileField(upload_to="portfolio_videos")


class PortfolioEditor(models.Model):
    htmlcontent = HTMLField()
    portfolio = models.ForeignKey(
        Portfolio, related_name="editors", on_delete=models.CASCADE
    )