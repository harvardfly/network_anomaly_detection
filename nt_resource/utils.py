from uuid import uuid4
from nt_resource.models import CatNormalResource


def add_normal_cat_data(data):
    """
    构建数据model  用yield每次返回1000条数据
    :param data
    :return:
    """
    tmp_cat_normal_models = []

    for cat_data in data:
        response_time = cat_data.get('response_time')
        request_count = cat_data.get('request_count') or 1
        fail_count = cat_data.get('fail_count') or 1
        cat_data['id'] = str(uuid4())
        if response_time < 1.2 and (fail_count / request_count) < 0.2:
            cat_obj = CatNormalResource(
                **cat_data
            )
            tmp_cat_normal_models.append(cat_obj)

        if len(tmp_cat_normal_models) >= 1000:
            yield tmp_cat_normal_models
            tmp_cat_normal_models = []

    yield tmp_cat_normal_models


def insert_normal_cat_data(data):
    """
    每次用bulk 批量插入 1000条数据
    :param data:
    :return:
    """
    for i in add_normal_cat_data(data):
        CatNormalResource.objects.bulk_create(i)
