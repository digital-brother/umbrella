import jwt
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from rest_framework import exceptions

User = get_user_model()


class DynamicRealmOIDCAuthentication(OIDCAuthentication):
    def get_access_token_payload(self, request):
        encoded_access_token = self.get_access_token(request)
        if not encoded_access_token:
            return None

        try:
            access_token_payload = jwt.decode(encoded_access_token, options={"verify_signature": False})
        except jwt.PyJWTError:
            msg = f"Invalid JWT token"
            raise exceptions.AuthenticationFailed(msg)

        return access_token_payload

    def get_cached_jwt_token_user(self, request):
        expiration = request.session.get('oidc_id_token_expiration', 0)
        now = time.time()
        if expiration > now:
            access_token_payload = self.get_access_token_payload(request)
            user = User.objects.get(email=access_token_payload['email'])
            return user

    def authenticate(self, request):
        user = self.get_cached_jwt_token_user(request)
        if user:
            return user, self.get_access_token(request)

        access_token_payload = self.get_access_token_payload(request)
        keycloak_realm_url = access_token_payload['iss']
        self.backend.OIDC_OP_TOKEN_ENDPOINT = settings.OIDC_OP_TOKEN_ENDPOINT_TEMPLATE.format(
            keycloak_realm_url=keycloak_realm_url)
        self.backend.OIDC_OP_USER_ENDPOINT = settings.OIDC_OP_USER_ENDPOINT_TEMPLATE.format(
            keycloak_realm_url=keycloak_realm_url)
        user, access_token = super().authenticate(request)

        request.session['oidc_id_token_expiration'] = access_token_payload['exp']
        return user, access_token
