from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.core.validators import RegexValidator
from shortuuid.django_fields import ShortUUIDField
from django.core.exceptions import ValidationError


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수입니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff") or not extra_fields.get("is_superuser"):
            raise ValueError("is_staff, is_superuser는 True로 설정해야 합니다.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=128)
    email = models.EmailField(unique=True)

    # RegexValidator를 사용하여 username 필드에 특수문자( . 제외)가 들어오지 않도록 설정
    username_validator = RegexValidator(
        regex=r"^[\w.]+$",
        message="유저명은 한글, 알파벳, 숫자, 밑줄 및 점만 포함할 수 있습니다.",
    )
    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[username_validator],
        error_messages={
            "unique": "이 유저명은 이미 사용 중입니다.",
        },
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    profile_picture = models.URLField(max_length=200, blank=True, null=True)

    # 전화번호 유효성 검사 010-1111-1111, 02-111-1111 지역번호까지 포함
    phone_regex = RegexValidator(
        regex=r"^\d{2,3}-\d{3,4}-\d{4}$",
        message="'010-1234-5678' 형식으로 입력해야 합니다.",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=13, blank=True
    )  # blank = True

    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_expert = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
