# web/authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from web.models import UserToken  # Tu modelo personalizado
from django.contrib.auth.models import User

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith("Token "):
            return None

        token = auth_header.split(" ")[1]

        try:
            token_obj = UserToken.objects.select_related('user').get(token=token)
        except UserToken.DoesNotExist:
            raise exceptions.AuthenticationFailed("Token inválido o no encontrado")

        if not token_obj.is_active:
            raise exceptions.AuthenticationFailed("Token inactivo")

        return (token_obj.user, token_obj)
