from django.db import models
from nt_core.models import BaseModel


class CatNormalResource(BaseModel):
    appid = models.IntegerField(blank=True, null=True)
    response_time = models.FloatField(blank=True, null=True)
    request_count = models.IntegerField(blank=True, null=True)
    fail_count = models.IntegerField(blank=True, null=True)
    click_num = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'cat_normal_resource'
