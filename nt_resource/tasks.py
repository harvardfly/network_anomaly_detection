from web.celery import app as celery_app
from nt_core.exceptions import RsError


@celery_app.task
def insert_es_question_task(qid):
    """
    使用异步任务执行试题插入
    :param qid:
    :return:
    """
    from rs_question.views import EsQuestionInsert
    try:
        EsQuestionInsert.es_question_insert(qid)
    except Exception as e:
        print(e)
        raise RsError('试题插入ES数据库失败')


@celery_app.task(bind=True, default_retry_delay=60, max_retries=2)
def insert_dt(self):
    print("----- not implemented ------")
    pass
