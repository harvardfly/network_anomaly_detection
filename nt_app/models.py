from django.db import models
from nt_core.models import BaseModel


class CatResource(BaseModel):
    appid = models.IntegerField(blank=True, null=True)
    response_time = models.FloatField(blank=True, null=True)
    request_count = models.IntegerField(blank=True, null=True)
    fail_count = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'cat_resource'
