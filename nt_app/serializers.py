from rest_framework import serializers
from nt_app.models import CatResource
from nt_core.exceptions import RsError
from nt_core.utils import get_current_timestamp


class CatResourceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatResource
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.appid = validated_data.get('appid', instance.appid)
        instance.response_time = validated_data.get(
            'response_time', instance.response_time
        )

        instance.update_time = get_current_timestamp()
        instance.save()
        return instance


class CatResourceCreateSerializer(serializers.Serializer):
    appid = serializers.IntegerField(required=True)
    response_time = serializers.FloatField(required=True)
    request_count = serializers.IntegerField(required=True)
    fail_count = serializers.IntegerField(required=True)

    def validate(self, attrs):
        request_count = attrs.get('request_count')
        fail_count = attrs.get('fail_count')
        if fail_count > request_count:
            raise RsError("失败次数不能大于请求数")

        return attrs
