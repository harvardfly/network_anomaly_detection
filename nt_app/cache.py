# coding:utf-8
import time
from django.core.cache import cache

CACHE_TIMEOUT_DEFAULT = 7 * 24 * 60 * 60


# def get_cognition_num(name, subject, faculty):
#     """
#     请求公库接口，根据认知点名字、学科获取认知点num
#     :param name:
#     :param subject:
#     :param faculty:
#     :return:
#     """
#     key = 'GET_COGNITION_NUM_{0}_{1}_{2}'.format(
#         hash(name), subject, faculty
#     )
#     content = cache.get(key)
#     if not content:
#         cog_num_url = settings.GET_COGNITION_NUM_URI.format(
#             settings.RS_SETTINGS['PUBLIC_HOST'],
#             name, subject
#         )
#         params = {
#             'name': name,
#             'subject': subject,
#             'faculty': faculty
#         }
#
#         content = request_with_token(
#             'get',
#             cog_num_url,
#             params=params
#         )
#         cache.set(key, content, timeout=CACHE_TIMEOUT_DEFAULT)
#
#     return content
