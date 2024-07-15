from django.db import models
from apps.users.models import CustomUser
import uuid


class Portfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expert = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    price = models.IntegerField()
    portfolio_start = models.DateTimeField()
    portfolio_end = models.DateTimeField()
    show = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_duration(self):
        return self.portfolio_end - self.portfolio_start
    


class PortfolioImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    portfolio = models.ForeignKey(
        Portfolio, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="portfolio_images")


class PortfolioVideo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    portfolio = models.ForeignKey(
        Portfolio, related_name="videos", on_delete=models.CASCADE
    )
    video = models.FileField(upload_to="portfolio_videos")
