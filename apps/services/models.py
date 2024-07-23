from django.db import models
from django.contrib.auth import get_user_model
from shortuuid.django_fields import ShortUUIDField

User = get_user_model()


class Category(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CategoryDetail(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Service(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    category_detail = models.ForeignKey(CategoryDetail, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="liked_services", blank=True)

    def __str__(self):
        return self.service_name


class PriceOption(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.IntegerField()
    price_option_name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.price_option_name


class Review(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="service_reviews"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )  # 리뷰 댓글은 User 모델로 추상화
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReviewComment(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # 리뷰 댓글은 User 모델로 추상화
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    price_option = models.ForeignKey(PriceOption, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def service(self):
        return self.price_option.service