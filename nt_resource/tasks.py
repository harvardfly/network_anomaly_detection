from web.celery import app as celery_app
from nt_core.exceptions import RsError
from nt_resource.utils import (
    add_cat_data,
    add_normal_cat_data
)
from nt_resource.models import CatNormalResource


@celery_app.task
def insert_cat_data(start_time, end_time):
    """
    使用异步,批量插入指定时间段的cat数据
    :param start_time:
    :param end_time:
    :return:
    """
    try:
        for i in add_cat_data(start_time, end_time):
            CatNormalResource.objects.bulk_create(i)
    except Exception as e:
        print(e)
        raise RsError('插入数据库失败')


@celery_app.task
def insert_normal_cat_data(data):
    """
    使用异步，每次用bulk 批量插入 1000条数据
    :param data:
    :return:
    """
    try:
        for i in add_normal_cat_data(data):
            CatNormalResource.objects.bulk_create(i)
    except Exception as e:
        print(e)
        raise RsError('插入数据库失败')


@celery_app.task(bind=True, default_retry_delay=60, max_retries=2)
def insert_dt(self):
    print("----- not implemented ------")
    pass
