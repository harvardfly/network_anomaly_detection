from django.conf.urls import url

from nt_account.views import (
    GenerateTokenView
)

urlpatterns = [
    # search question
    url(r'^generate_token$',
        GenerateTokenView.as_view()),
]
