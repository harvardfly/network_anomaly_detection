import time
import datetime
from operator import itemgetter
import cgi
from xml.sax.saxutils import unescape


def get_current_timestamp():
    """
    获取当前时间戳
    :return:
    """
    return int(time.time()) * 1000


def convert_timestamp_to_datetime(timestamp):
    """
    把时间戳转换为datetime
    :param timestamp:
    :return:
    """
    time_array = datetime.datetime.utcfromtimestamp(timestamp / 1000)
    return str(time_array)


def object_list_to_dict(obj_list, primary_key='id'):
    """
    将list 转化为以primary_key为key的dict
    :param obj_list:
    :param primary_key:
    :return:
    """
    result = {}
    for obj in obj_list:
        key = obj.__getattribute__(primary_key)
        result[key] = obj

    return result


def get_int_or_none(val):
    try:
        return int(val)
    except Exception:
        return None


def get_sort_data(data, str_key, reverse=False):
    """
    多字典列表按sort顺序排序
    :param data:
    :param str_key:
    :param reverse:
    :return:
    """
    data = sorted(
        data,
        key=itemgetter(str_key),
        reverse=reverse
    )[:len(data)]
    return data


def sort_to_choice_letter(sort_num):
    """
    将数字转换为对应的26个字母
    :param sort_num:
    :return:
    """
    sort_to_choice_map = dict((x, chr(ord('A') + x)) for x in range(26))
    sort_num = get_int_or_none(sort_num)

    return sort_to_choice_map.get(sort_num) or None


def diff_two_list(list1, list2):
    """
    两个list对应元素相减 list1对应位置元素与list2对应位置元素相减
    先将两个列表压缩成元组
    :param list1:
    :param list2:
    :return:
    """
    return list(map(lambda x: x[0] - x[1], zip(list1, list2)))


def get_two_list_differences(list1, list2):
    """
    list1与list2的差集  在list1里面但不在list2里面
    :param list1:
    :param list2:
    :return:
    """
    return list(set(list1).difference(set(list2)))


def get_two_list_intersection(list1, list2):
    """
    list1与list2的交集
    :param list1:
    :param list2:
    :return:
    """
    return list(set(list1).intersection(set(list2)))


def get_two_list_union(list1, list2):
    """
    list1与list2的并集
    :param list1:
    :param list2:
    :return:
    """
    return list(set(list1).union(set(list2)))


def get_cgi_data(data):
    """
    防止xss注入  对数据处理
    quote表示是否要转换引号
    处理后入库
    :param data:
    :return:
    """
    # data = '<img src="null" onerror="alert(document.cookie)" />'
    cgi_data = cgi.escape(
        data,
        quote=True
    )
    return cgi_data


def get_unescape_data(cgi_data):
    """
    从数据库拿出时，先解密
    将处理后的cgi_data恢复为原data
    :param cgi_data:
    :return:
    """
    unescape_data = unescape(
        cgi_data,
        {"&apos;": "'", "&quot;": '"'}
    )
    return unescape_data
