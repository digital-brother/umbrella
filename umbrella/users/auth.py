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

    def authenticate_cached(self, request):
        token_is_cached = request.session.get('oidc_access_token') == self.get_access_token(request)
        token_is_active = request.session.get('oidc_id_token_expiration', 0) > time.time()
        if token_is_active and token_is_cached:
            access_token = request.session['oidc_access_token']
            user_id = request.session['oidc_user_id']
            user = User.objects.get(id=user_id)
            return user, access_token
        return None, None

    def authenticate(self, request):
        user, access_token = self.authenticate_cached(request)
        if user and access_token:
            return user, access_token

        access_token_payload = self.get_access_token_payload(request)
        self.backend.OIDC_OP_TOKEN_ENDPOINT = settings.OIDC_OP_TOKEN_ENDPOINT_TEMPLATE.format(
            keycloak_realm_url=access_token_payload['iss'])
        self.backend.OIDC_OP_USER_ENDPOINT = settings.OIDC_OP_USER_ENDPOINT_TEMPLATE.format(
            keycloak_realm_url=access_token_payload['iss'])
        user, access_token = super().authenticate(request)

        request.session['oidc_id_token_expiration'] = access_token_payload['exp']
        request.session['oidc_access_token'] = access_token
        request.session['oidc_user_id'] = str(user.id)
        return user, access_token
