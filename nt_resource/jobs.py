# -*- coding: utf-8 -*-
import logging
import datetime

from nt_app.cache import get_cache_cat_data
from nt_resource.tasks import insert_normal_cat_data
from nt_core.utils import (
    get_current_timestamp,
    convert_datetime_to_timestamp
)

logger = logging.getLogger(__name__)


def my_scheduled_job():
    logger.info('my_scheduled_job  ....')


def insert_normal_cat_job():
    """
    定时导入前一天的正常数据
    :return:
    """
    logger.info('insert_normal_cat_job  ....')
    dt_time = datetime.datetime.now() + datetime.timedelta(days=-1)
    start_time = convert_datetime_to_timestamp(dt_time)
    end_time = get_current_timestamp()
    data = get_cache_cat_data(start_time, end_time)
    insert_normal_cat_data.delay(data)
