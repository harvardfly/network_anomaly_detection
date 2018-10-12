from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置DJANGO模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings_local')
from django.conf import settings  # noqa

app = Celery(settings.CELERY_SETTINGS['namespace'])
app.config_from_object(
    'django.conf:settings',
    namespace=settings.CELERY_SETTINGS['namespace']
)
app.conf.broker_url = settings.CELERY_SETTINGS['broker_url']
app.conf.result_backend = settings.CELERY_SETTINGS['result_backend']
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
