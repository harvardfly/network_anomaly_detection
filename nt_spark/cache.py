# coding:utf-8
from django.core.cache import cache
from nt_spark.utils import get_kmeans_result

CACHE_TIMEOUT_DEFAULT = 7 * 24 * 60 * 60


def get_cache_kmeans_result(appid, start_time, end_time, force=False):
    """
    获取appid指定时间段的cat数据
    :param appid:
    :param start_time:
    :param end_time:
    :param force:
    :return:
    """
    key = 'GET_KMEANS_RESULT_{0}_FROM_{1}_TO_{2}'.format(
        appid, start_time, end_time
    )
    print(key)
    content = cache.get(key)
    if force or not content:
        content = get_kmeans_result(appid, start_time, end_time)
        if content:
            cache.set(key, content, timeout=CACHE_TIMEOUT_DEFAULT)

    return content
