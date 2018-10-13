# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.views import APIView
from nt_core.exceptions import RsError
from nt_core.utils import get_int_or_none
from nt_spark.cache import get_cache_kmeans_result


class CatResultDataView(APIView):
    def post(self, request):
        req_data = request.data
        start_time = get_int_or_none(req_data.get('start_time'))
        end_time = get_int_or_none(req_data.get('end_time'))
        appid = get_int_or_none(req_data.get('appid'))
        if not all([start_time, end_time, appid]):
            raise RsError('缺少必要参数')

        algorithm_name = req_data.get('algorithm_name')
        if algorithm_name not in ["kmeans", "svdd", "random_forest"]:
            raise RsError("algorithm_name不存在")

        ser_data = get_cache_kmeans_result(appid, start_time, end_time)
        return Response(ser_data)
