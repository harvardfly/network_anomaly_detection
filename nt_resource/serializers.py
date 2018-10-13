from rest_framework import serializers
from nt_resource.models import CatNormalResource
from nt_core.utils import get_current_timestamp


class CatNormalResourceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatNormalResource
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.appid = validated_data.get('appid', instance.appid)
        instance.response_time = validated_data.get(
            'response_time', instance.response_time
        )

        instance.update_time = get_current_timestamp()
        instance.save()
        return instance
