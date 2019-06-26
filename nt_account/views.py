# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from nt_core.exceptions import RsError
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes
from nt_core.auto_schema import RsSchema


@authentication_classes([])
class GenerateTokenView(APIView):
    """
    post:
    <pre>生成用户接口的 TOKEN 字符串</pre>
    """
    permission_classes = [AllowAny, ]
    docs = {
        'post-form': [
            ('username', '使用用户名和密码生成'),
            ('password', '使用用户名和密码生成'),
            ('token', '使用TOKEN生成，如果TOKEN和用户信息都存在，TOKEN优先使用'),
        ]
    }
    schema = RsSchema(docs=docs)

    def post(self, request):
        req_data = request.data

        token_string = req_data.get('token')
        username = req_data.get('username')
        password = req_data.get('password')
        if not token_string:
            auth_user = authenticate(username=username, password=password)
        else:
            token_obj = Token.objects.select_related('user').filter(
                key=token_string
            ).first()
            if token_obj:
                auth_user = token_obj.user
            else:
                raise RsError('生成token失败，请检查token值')

        if auth_user:
            Token.objects.filter(user=auth_user).delete()
            token = Token.objects.create(user=auth_user)

            return Response({
                'token': token.key
            })
        else:
            raise RsError('生成token失败，请检查token值或用户信息')
