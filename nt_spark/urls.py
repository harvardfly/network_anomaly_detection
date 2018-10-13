from django.conf.urls import url
from nt_spark.views import (
    CatResultDataView
)

urlpatterns = [
    url(r'^cat_result$', CatResultDataView.as_view()),
]
