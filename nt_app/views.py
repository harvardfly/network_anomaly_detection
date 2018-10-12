# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from nt_core.exceptions import RsError

from nt_app.models import CatResource
from nt_app.serializers import (
    CatResourceCreateSerializer,
    CatResourceListSerializer
)


class CatResourceView(APIView):
    def post(self, request):
        req_data = request.data
        validate_param = CatResourceCreateSerializer(data=req_data)
        validate_param.is_valid(raise_exception=True)
        data = validate_param.validated_data

        cat_obj = CatResource.objects.create(
            **data
        )

        return Response({
            'id': cat_obj.id
        })

    def get(self, request):
        req_data = request.GET
        _id = req_data.get('id')
        if not _id:
            raise RsError('id不可缺少')

        cat_obj = CatResource.objects.filter(
            id=_id
        ).first()
        if not cat_obj:
            raise RsError('数据不存在')
        ser_data = CatResourceListSerializer(cat_obj).data
        return Response(ser_data)

    def put(self, request):
        req_data = request.data
        _id = req_data.get('id')
        if not _id:
            raise RsError('id不可缺少')

        cat_obj = CatResource.objects.filter(id=_id).first()
        if not cat_obj:
            raise RsError("id不存在")

        ser = CatResourceListSerializer(cat_obj, req_data, partial=True)

        if ser.is_valid():
            ser.save()
        else:
            raise RsError(ser.errors)

        return Response({"result": True, "id": _id})

    def delete(self, request):
        req_data = request.data
        delete_ids = req_data.get('delete_ids')
        rows = CatResource.objects.filter(
            id__in=delete_ids
        ).delete()
        return Response({"result": True, "rows": rows})


class CatResourceListView(ListAPIView):
    cat_search_fields = [
        'appid', 'id', 'response_time', 'request_count',
        'start_time', 'end_time', 'fail_count'
    ]

    serializer_class = CatResourceListSerializer

    def list(self, request, *args, **kwargs):
        filters = self.generate_filter(request)
        cat_lists = CatResource.objects.filter(**filters).order_by('-update_time')
        page_data = self.paginate_queryset(cat_lists)
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
