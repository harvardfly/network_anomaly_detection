from django.db import models
from nt_core.models import BaseModel


class CatResultData(BaseModel):
    appid = models.IntegerField(blank=True, null=True)


    class Meta:
        db_table = 'cat_normal_resource'
