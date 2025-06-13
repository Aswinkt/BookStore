from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import uuid

class BaseInfoModel(models.Model):
    """
    Base fields for all model
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_created",
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_updated",
        null=True,
    )
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseInfoModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=65)
    is_active = models.BooleanField(default=True)
    is_author = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)

class Author(BaseInfoModel):
    object_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Public identifier',
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="%(app_label)s_%(class)s_user",
        null=True, 
        blank=True
    )
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(BaseInfoModel):
    object_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Public identifier',
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name="%(app_label)s_%(class)s_author",
        null=True, 
        blank=True
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published_date = models.DateField()

    def __str__(self):
        return self.title

class RequestLog(BaseInfoModel):
    method = models.CharField(max_length=10)
    path = models.TextField()
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_user",
        null=True, 
        blank=True
    )