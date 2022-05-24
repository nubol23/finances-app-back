import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import CIEmailField
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, save=True):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        if save:
            user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password=password, save=False)

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)

        return user


class User(PermissionsMixin, AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = CIEmailField(verbose_name="email address", max_length=255, unique=True)
    name = models.CharField(max_length=150)

    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        default=False,
        help_text="Designate whether this user should be treated as active."
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        ordering = ("-created_on",)

    def __str__(self):
        return f"{self.name} <{self.email}>"
