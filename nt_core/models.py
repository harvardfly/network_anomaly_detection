import time
from uuid import uuid4
from django.db import models


def get_current_time_bigint():
    return int(time.time()) * 1000


class BaseModel(models.Model):
    id = models.CharField(
        primary_key=True, max_length=40, default=uuid4, editable=False
    )
    create_time = models.BigIntegerField(default=get_current_time_bigint)
    update_time = models.BigIntegerField(default=get_current_time_bigint)

    def save(self, *args, **kwargs):
        self.update_time = get_current_time_bigint()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
