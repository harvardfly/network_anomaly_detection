from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=30, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=6,
        choices=(("male", u"男"), ("female", "女")),
        default="female"
    )
    mobile = models.CharField(
        null=True, blank=True, max_length=11
    )
    email = models.EmailField(
        max_length=100, null=True, blank=True
    )

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
