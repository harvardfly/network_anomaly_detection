from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import (
    jwt_encode_handler, jwt_payload_handler
)
from nt_account.permissions import IsOwnerOrReadOnly
from nt_user.models import UserFeedbackMessage
from nt_user.serializers import (
    UserRegSerializer, UserDetailSerializer,
    FeedbackMessageSerializer
)

User = get_user_model()


class UserViewset(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (
        JSONWebTokenAuthentication,
        authentication.SessionAuthentication
    )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(
            re_dict,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def get_object(self):
        return self.request.user


class FeedbackMessageViewset(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    list:
        获取用户反馈
    create:
        添加反馈
    delete:
        删除反馈
    retrieve:
    用户反馈详情
    """
    serializer_class = FeedbackMessageSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_queryset(self):
        return UserFeedbackMessage.objects.filter(
            user=self.request.user
        )


class ReturnUrlView(APIView):
    def get(self, request):
        req_data = request.GET
        return Response({"HELLO": "WORLD"})
