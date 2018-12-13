from nt_user.views import (
    UserViewset,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    r'^users',
    UserViewset,
    base_name="users"
)

# GET nt_user/users/12/  详情

urlpatterns = [
]

urlpatterns += router.urls
