from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from nt_core.exceptions import RsError

from nt_resource.models import CatNormalResource
from nt_resource.serializers import (
    CatNormalResourceListSerializer
)


class CatNormalResourceView(APIView):
    def get(self, request):
        req_data = request.GET
        _id = req_data.get('id')
        if not _id:
            raise RsError('id不可缺少')

        cat_normal_obj = CatNormalResource.objects.filter(
            id=_id
        ).first()
        if not cat_normal_obj:
            raise RsError('数据不存在')
        ser_data = CatNormalResourceListSerializer(cat_normal_obj).data
        return Response(ser_data)

    def put(self, request):
        req_data = request.data
        _id = req_data.get('id')
        if not _id:
            raise RsError('id不可缺少')

        cat_normal_obj = CatNormalResource.objects.filter(id=_id).first()
        if not cat_normal_obj:
            raise RsError("id不存在")

        ser = CatNormalResourceListSerializer(
            cat_normal_obj, req_data, partial=True
        )

        if ser.is_valid():
            ser.save()
        else:
            raise RsError(ser.errors)

        return Response({"result": True, "id": _id})

    def delete(self, request):
        req_data = request.data
        delete_ids = req_data.get('delete_ids')
        rows = CatNormalResource.objects.filter(
            id__in=delete_ids
        ).delete()
        return Response({"result": True, "rows": rows})


class CatNormalResourceListView(ListAPIView):
    cat_search_fields = [
        'appid', 'id', 'response_time', 'request_count',
        'start_time', 'end_time', 'fail_count'
    ]

    serializer_class = CatNormalResourceListSerializer

    def list(self, request, *args, **kwargs):
        filters = self.generate_filter(request)
        cat_normal_lists = CatNormalResource.objects.filter(
            **filters
        ).order_by('-update_time')
        page_data = self.paginate_queryset(cat_normal_lists)
        serializer = self.serializer_class(page_data, many=True)

        return self.get_paginated_response(serializer.data)

    def generate_filter(self, request):
        req_data = request.GET
        filters = {}
        for filed in self.cat_search_fields:
            field_val = req_data.get(filed)
            if field_val:
                if filed in ['id', 'appid']:
                    filters[filed] = field_val
                elif filed in ['start_time']:
                    filters['create_time__gt'] = field_val
                elif filed in ['end_time']:
                    filters['create_time__lt'] = field_val
                elif filed in ['response_time', 'request_count', 'fail_count']:
                    filters['{}__gte'.format(filed)] = field_val
                    filters['{}__lte'.format(filed)] = field_val

        return filters
