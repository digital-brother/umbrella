import jwt
from django.conf import settings
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from rest_framework import exceptions


class DynamicRealmOIDCAuthentication(OIDCAuthentication):
    def get_realm_url_from_jwt_token(self, request):
        encoded_access_token = self.get_access_token(request)
        if not encoded_access_token:
            return None

        access_token = jwt.decode(encoded_access_token, options={"verify_signature": False})
        keycloak_realm_url = access_token.get('iss')

        if not keycloak_realm_url:
            msg = 'JWT token iss field is not present or empty'
            raise exceptions.AuthenticationFailed(msg)

        return keycloak_realm_url

    def authenticate(self, request):
        keycloak_realm_url = self.get_realm_url_from_jwt_token(request)
        self.backend.OIDC_OP_TOKEN_ENDPOINT = settings.OIDC_OP_TOKEN_ENDPOINT_TEMPLATE.format(
            keycloak_realm_url=keycloak_realm_url)
        self.backend.OIDC_OP_USER_ENDPOINT = settings.OIDC_OP_USER_ENDPOINT_TEMPLATE.format(
            keycloak_realm_url=keycloak_realm_url)
        return super().authenticate(request)
