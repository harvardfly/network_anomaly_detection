from django.conf.urls import url
from nt_resource.views import (
    CatNormalResourceView,
    CatNormalResourceListView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    r'^cat_normal_list',
    CatNormalResourceListView,
    base_name="cat_normal_list"
)

urlpatterns = [
    url(r'^cat_normal_resource$', CatNormalResourceView.as_view()),
    # url(r'^cat_normal_list$', cat_list),
]

urlpatterns += router.urls
