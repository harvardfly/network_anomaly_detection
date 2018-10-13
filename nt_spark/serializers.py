from rest_framework import serializers
from nt_spark.models import CatResultData


class CatResultDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatResultData
        fields = '__all__'
