from rest_framework.exceptions import APIException
from rest_framework import status


class RsError(APIException):
    """
    自定义Exception
    """
    status_code = status.HTTP_200_OK
    default_detail = '未知错误，请联系管理员.'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail

        self.detail = detail

    def __str__(self):
        return self.detail
