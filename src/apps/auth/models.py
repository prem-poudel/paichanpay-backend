from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from src.apps.common.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self.create_user(email, password, **extra_fields)


class User(BaseModel, AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=255, unique=True)

    # Optional Information
    first_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)

    # Media
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    # # Permissions
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)

    objects: UserManager = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number", "birth_date", "address"]

    def __str__(self):
        return self.username


class UserModelMixin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True
