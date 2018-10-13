"""ccnu_data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from rest_framework.documentation import include_docs_urls
from nt_account.authentication_doc import NtAuthenticationDoc
from rest_framework.permissions import AllowAny

urlpatterns = [
    url(r'^docs/', include_docs_urls(
        title='API接口文档',
        authentication_classes=(NtAuthenticationDoc,),
        permission_classes=(AllowAny,)
    )),
    url(r'^nt_account/', include('nt_account.urls')),
    url(r'^nt_app/', include('nt_app.urls')),
    url(r'^nt_resource/', include('nt_resource.urls')),
    url(r'^nt_spark/', include('nt_spark.urls')),
]
