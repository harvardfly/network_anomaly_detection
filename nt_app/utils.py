from nt_app.models import CatResource
from nt_app.serializers import CatResourceListSerializer


def get_cat_res_data(start_time, end_time):
    """
    获取特定时间段的cat数据
    :param start_time:
    :param end_time:
    :return:
    """
    cat_objs = CatResource.objects.filter(
        create_time__gt=start_time,
        update_time__lt=end_time
    ).all()
    ser_data = CatResourceListSerializer(cat_objs, many=True).data
    return ser_data
