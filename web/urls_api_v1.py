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
from rest_framework.permissions import AllowAny
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^docs/', include_docs_urls(
        title='API接口文档',
        permission_classes=(AllowAny,)
    )),
    # rest_framework自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # rest_framework自带的登录
    url(r'^api-auth/', include(
        'rest_framework.urls',
        namespace='rest_framework')
        ),

    # jwt的认证接口
    url(r'^login/$', obtain_jwt_token),

    url(r'^nt_user/', include('nt_user.urls')),
    url(r'^nt_account/', include('nt_account.urls')),
    url(r'^nt_app/', include('nt_app.urls')),
    url(r'^nt_resource/', include('nt_resource.urls')),
    url(r'^nt_spark/', include('nt_spark.urls')),
    # 第三方登录url
    url('', include('social_django.urls', namespace='social')),
]
