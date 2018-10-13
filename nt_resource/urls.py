from django.conf.urls import url
from nt_resource.views import (
    CatNormalResourceView,
    CatNormalResourceListView
)

urlpatterns = [
    url(r'^cat_normal_resource$', CatNormalResourceView.as_view()),
    url(r'^cat_normal_list$', CatNormalResourceListView.as_view()),
]
