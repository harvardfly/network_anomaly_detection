from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token
from nt_core.exceptions import RsError
from nt_core.utils import get_current_timestamp
from nt_account.tasks import save_api_record_task
import json


class NtAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Bearer'

    def authenticate(self, request):
        http_auth = request.META.get('HTTP_AUTHORIZATION', None)

        if http_auth:
            auth_arr = http_auth.split(' ')
        else:
            raise RsError('需要token认证')

        if len(auth_arr) != 2:
            raise RsError('Token认证格式出错')

        if auth_arr[0] != self.keyword:
            raise RsError('Token认证模式为{0}'.format(self.keyword))

        return self.authenticate_credentials(request, auth_arr[1])

    def authenticate_credentials(self, request, token):
        token_obj = Token.objects.select_related('user').filter(
            key=token
        ).first()

        if not token_obj:
            raise RsError('Token不合法，找不到对应的Token用户')

        if not token_obj.user.is_active:
            raise RsError('Token用户处于非激活状态')

        # 赋值用户信息
        user_obj = token_obj.user
        request.user = user_obj

        # 记录用户的请求信息
        # self.record_api_history(request)
        return token_obj.user, token_obj

    def authenticate_header(self, request):
        return self.keyword

    def record_api_history(self, request):
        request_info = request.META
        user_obj = request.user

        remote_addr = request_info.get('REMOTE_ADDR', None)
        method = request_info.get('REQUEST_METHOD', None)
        path_info = request_info.get('PATH_INFO', None)
        query_string = request_info.get('QUERY_STRING', None)

        # 验证用户有没有功资源平台的权限
        if not user_obj.is_superuser and 'rs_public' in path_info:
            raise RsError('用户权限禁止访问资源数据')

        # 获得post data
        post_data = request.data
        if len(post_data) > 0:
            post_data = json.dumps(post_data)
        else:
            post_data = None

        data = {
            'create_time': get_current_timestamp(),
            'update_time': get_current_timestamp(),
            'user_id': user_obj.id,
            'remote_addr': remote_addr,
            'method': method,
            'app_url': "/".join(path_info.split("/")[2:4]),
            'path_info': path_info,
            'query_string': query_string,
            'post_data': post_data,
        }
        save_api_record_task.delay(data)
