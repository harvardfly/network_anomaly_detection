from django.conf.urls import url
from nt_app.views import (
    CatResourceView,
    CatResourceListView
)

urlpatterns = [
    url(r'^cat_resource$', CatResourceView.as_view()),
    url(r'^cat_list$', CatResourceListView.as_view()),
]
