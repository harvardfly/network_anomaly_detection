import django_filters
from django.db.models import Q

from nt_resource.models import CatNormalResource


class CatNormalResourceFilter(django_filters.rest_framework.FilterSet):
    """
    的过滤类
    """
    min_count = django_filters.NumberFilter(
        field_name='fail_count',
        help_text="最小失败次数",
        lookup_expr='gte'
    )

    max_count = django_filters.NumberFilter(
        field_name='fail_count',
        help_text="最大失败次数",
        lookup_expr='lte'
    )
    normal_cat = django_filters.NumberFilter(method='normal_cat_filter')

    def normal_cat_filter(self, queryset, name, value):
        """
        定义异常指标 值可以是response_time、request_count或者fail_count
        :param queryset:
        :param name:
        :param value:
        :return:
        """
        return queryset.filter(
            Q(response_time=value) |
            Q(request_count=value) |
            Q(fail_count=value)
        )

    class Meta:
        model = CatNormalResource
        fields = [
            "min_count", "max_count",
            "appid", "response_time",
            "request_count", "fail_count"
        ]
