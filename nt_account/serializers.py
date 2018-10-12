from rest_framework import serializers
from nt_account.models import UserApiRecordHistory


class UserApiRecordHistorySer(serializers.ModelSerializer):
    class Meta:
        model = UserApiRecordHistory
        fields = '__all__'
