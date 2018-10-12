from django.db import models
from nt_core.models import BaseModel


class UserApiRecordHistory(BaseModel):
    user_id = models.IntegerField(blank=True, null=True)
    app_url = models.CharField(max_length=100, blank=True, null=True)
    path_info = models.CharField(max_length=500, blank=True, null=True)
    query_string = models.CharField(max_length=500, blank=True, null=True)
    post_data = models.CharField(max_length=500, blank=True, null=True)
    remote_addr = models.GenericIPAddressField(blank=True, null=True)
    method = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'api_record_history'
