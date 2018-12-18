import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from nt_user.models import UserFeedbackMessage

from nt_core.utils import REGEX_MOBILE

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """

    class Meta:
        model = User
        fields = (
            "id", "username", "gender",
            "birthday", "email", "mobile"
        )


class UserRegSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        label="用户名", help_text="用户名",
        required=True, allow_blank=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="用户已经存在"
            )
        ]
    )

    password = serializers.CharField(
        style={'input_type': 'password'},
        help_text="密码", label="密码",
        write_only=True,
    )

    def validate(self, attrs):
        mobile = attrs.get('mobile')

        if mobile:
            sms_validator = SmsSerializer(attrs)
            sms_validator.validate_mobile(mobile)
            attrs["mobile"] = mobile
        return attrs

    class Meta:
        model = User
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=User.objects.all(),
        #         fields=('username', 'mobile'),
        #         message="username或者mobile已经存在"
        #     )
        # ]
        fields = ("username", "mobile", "password")


class FeedbackMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFeedbackMessage
        fields = "__all__"
