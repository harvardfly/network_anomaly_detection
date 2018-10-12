from web.celery import app as celery_app
from nt_account.models import UserApiRecordHistory


@celery_app.task
def save_api_record_task(data):
    """
    保存用户使用的接口记录
    :param data:
    :return:
    """

    api_history = UserApiRecordHistory(**data)
    api_history.save()
