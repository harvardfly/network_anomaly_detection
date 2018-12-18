from django.conf.urls import url
from nt_user.views import (
    UserViewset, FeedbackMessageViewset, ReturnUrlView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    r'^users',
    UserViewset,
    base_name="users"
)

# GET nt_user/users/12/  详情

router.register(
    r'messages',
    FeedbackMessageViewset,
    base_name="messages"
)

urlpatterns = [
    url(r'^index$', ReturnUrlView.as_view())
]

urlpatterns += router.urls
