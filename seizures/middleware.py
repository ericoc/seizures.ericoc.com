from base64 import b64decode

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth.models import User


class SeizureHTTPBasicAuthMiddleware(RemoteUserMiddleware):

    def process_request(self, request):
        try:
            header = request.META.get('HTTP_AUTHORIZATION')
            if header:
                creds = b64decode(header.partition(' ')[2]).decode().split(':')
                user = authenticate(
                    request, username=creds[0], password=creds[1]
                )
                if user:
                    login(request=request, user=user)

        except User.DoesNotExist:
            logout(request)

        super().process_request(request)
