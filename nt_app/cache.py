# coding:utf-8
import time
from django.core.cache import cache
from nt_app.utils import get_cat_res_data


CACHE_TIMEOUT_DEFAULT = 7 * 24 * 60 * 60


def get_cache_cat_data(start_time, end_time, force=False):
    """
    获取指定时间段的cat数据
    :param start_time:
    :param end_time:
    :return:
    """
    key = 'GET_CAT_RES_DATA_{0}_TO_{1}'.format(
        start_time, end_time
    )
    content = cache.get(key)
    if force or not content:
        content = get_cat_res_data(start_time, end_time)
        if content:
            cache.set(key, content, timeout=CACHE_TIMEOUT_DEFAULT)

    return content
