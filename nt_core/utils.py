import time
import json
import urllib
import datetime
import requests
from operator import itemgetter
import cgi
from xml.sax.saxutils import unescape

REGEX_MOBILE = "^1[3456789]\d{9}$"


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


def convert_datetime_to_timestamp(dtime):
    """
    把datetime转换为时间戳
    :param datetime:
    :return:
    """
    timestamp = time.mktime(dtime.timetuple())
    return int(timestamp) * 1000


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


class OAuth_Base(object):  # 基类，将相同的方法写入到此类中
    def __init__(self, client_id, client_key, redirect_url):  # 初始化，载入对应的应用id、秘钥和回调地址
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_url = redirect_url

    def _get(self, url, data):  # get方法
        request_url = '%s?%s' % (url, urllib.parse.urlencode(data))
        response = urllib.request.urlopen(request_url)
        return response.read()

    def _post(self, url, data):  # post方法
        request = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(encoding='UTF8'))  # 1
        response = urllib.request.urlopen(request)
        return response.read()

    # 下面的方法，不同的登录平台会有细微差别，需要继承基类后重写方法

    def get_auth_url(self):  # 获取code
        pass

    def get_access_token(self, code):  # 获取access token
        pass

    def get_open_id(self):  # 获取openid
        pass

    def get_user_info(self):  # 获取用户信息
        pass

    def get_email(self):  # 获取用户邮箱
        pass


class OAuth_WEIBO(OAuth_Base):
    def get_auth_url(self):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_url,
            'scope': 'email',
            'state': 1
        }
        url = 'https://api.weibo.com/oauth2/authorize?{}'.format(
            urllib.parse.urlencode(params)
        )
        return url

    def get_access_token(self, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_key,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_url
        }
        response = requests.post(
            'https://api.weibo.com/oauth2/access_token',
            data=params
        )
        result = json.loads(response.decode('utf-8'))
        self.access_token = result["access_token"]
        self.openid = result["uid"]
        return self.access_token

    def get_open_id(self):  # 新浪的openid在之前get_access_token（）方法中已经获得
        return self.openid

    def get_user_info(self):
        params = {
            'access_token': self.access_token,
            'uid': self.openid,
        }
        response = requests.get(
            'https://api.weibo.com/2/users/show.json',
            params=params
        )
        result = json.loads(response.decode('utf-8'))
        return result

    def get_email(self):
        params = {'access_token': self.access_token}
        response = self._get(
            'https://api.weibo.com/2/account/profile/email.json',
            params
        )
        result = json.loads(response.decode('utf-8'))
        return result[0]['email']
