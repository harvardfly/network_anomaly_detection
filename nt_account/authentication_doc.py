from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import AnonymousUser


class NtAuthenticationDoc(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Bearer'

    def authenticate(self, request):
        return AnonymousUser(), None
