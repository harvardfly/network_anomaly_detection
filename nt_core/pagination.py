# -*- coding: utf-8 -*-
from rest_framework.views import Response
from rest_framework import pagination
from django.utils import six
from django.core.paginator import InvalidPage


class RsPagination(pagination.PageNumberPagination):
    page_size_query_param = 'per_page'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)

        # 对于某些自定义的分页类，需要读取per_page参数
        page_size = request.data.get(self.page_size_query_param, page_size)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        if 'page' in request.data:
            page_number = request.data.get('page')
        else:
            page_number = request.query_params.get(self.page_query_param, 1)

        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            # raise NotFound(msg)
            page_number = 1
            self.page = paginator.page(page_number)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        page = self.page.number
        last = self.page.paginator.num_pages
        next_page = last if last == page else page + 1
        count = self.page.paginator.count

        return Response({
            'results': data,
            'next': next_page,
            'page': page,
            'last': last,
            'count': count,
        })
