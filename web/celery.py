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



# import os
# from celery import Celery
# from django.apps import apps, AppConfig
# from django.conf import settings
#
# if not settings.configured:
#     # set the default Django settings module for the 'celery' program.
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings_local')  # pragma: no cover
#
# app = Celery('')
# # Using a string here means the worker will not have to
# # pickle the object when using Windows.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
#
# class CeleryAppConfig(AppConfig):
#     name = 'taskapp'
#     verbose_name = 'Celery Config'
#
#     def ready(self):
#         installed_apps = [app_config.name for app_config in apps.get_app_configs()]
#         app.autodiscover_tasks(lambda: installed_apps, force=True)
#
#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {self.request!r}')  # pragma: no cover
