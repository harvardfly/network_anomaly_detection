from django.db import models
from django.contrib.auth.models import AbstractUser
from nt_core.models import BaseModel


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


class UserFeedbackMessage(BaseModel):
    """
    咨询反馈
    """
    MESSAGE_CHOICES = (
        (1, "咨询"),
        (2, "算法反馈"),
        (3, "建议")
    )
    user = models.ForeignKey(
        UserProfile, verbose_name="用户", on_delete=True
    )
    message_type = models.IntegerField(
        default=1, choices=MESSAGE_CHOICES, verbose_name="反馈类型",
        help_text=u"反馈类型: 1(咨询),2(算法反馈),3(建议)"
    )
    topic = models.CharField(
        max_length=100, default="", verbose_name="主题"
    )
    message = models.TextField(
        default="", verbose_name="反馈内容", help_text="反馈内容"
    )
    file = models.FileField(
        upload_to="message/images/",
        verbose_name="上传的文件",
        help_text="上传的文件"
    )

    class Meta:
        verbose_name = "用户反馈"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.topic
