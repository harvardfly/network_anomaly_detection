from django.db import models
from nt_core.models import BaseModel
from jsonfield import JSONField


class CatResultData(BaseModel):
    appid = models.IntegerField(blank=True, null=True)
    algorithm_name = models.CharField(
        max_length=50, blank=True, null=True
    )
    start_time = models.BigIntegerField()
    end_time = models.BigIntegerField()
    result_data = JSONField(blank=True, null=True)

    class Meta:
        db_table = 'cat_result_data'
