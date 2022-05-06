import time

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from rest_framework import exceptions

from umbrella.users.models import Group

User = get_user_model()


def decode_token(encoded_access_token):
    try:
        access_token_payload = jwt.decode(encoded_access_token, options={"verify_signature": False})
        return access_token_payload
    except jwt.PyJWTError:
        msg = "Invalid JWT token"
        raise exceptions.AuthenticationFailed(msg)


class DynamicRealmOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    groups_claim = 'groups'

    def create_user(self, claims):
        """Return object for a newly created user account."""
        email = claims.get('email')
        username = self.get_username(claims)
        user = self.UserModel.objects.create_user(username, email=email, realm=self.realm)
        self.update_user(user, claims)
        return user

    def update_user(self, user, claims):
        if self.groups_claim not in claims:
            return user

        group_names = claims[self.groups_claim]
        groups = [Group.create_keycloak_group_and_tag(group_name=group_name)
                  for group_name in group_names]
        user.groups.set(groups)
        return user

    def get_or_create_user(self, access_token, id_token, payload):
        access_token_payload = decode_token(access_token)
        self.realm = access_token_payload['iss'].split('/')[-1]
        return super().get_or_create_user(access_token, id_token, payload)


class DynamicRealmOIDCAuthentication(OIDCAuthentication):
    keyword = 'Bearer'

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

        encoded_access_token = self.get_access_token(request)
        if not encoded_access_token:
            return None

        access_token_payload = decode_token(encoded_access_token)
        self.backend.OIDC_OP_TOKEN_ENDPOINT = settings.OIDC_OP_TOKEN_ENDPOINT_TEMPLATE.format(
            keycloak_realm_url=access_token_payload['iss'])
        self.backend.OIDC_OP_USER_ENDPOINT = settings.OIDC_OP_USER_ENDPOINT_TEMPLATE.format(
            keycloak_realm_url=access_token_payload['iss'])
        user, access_token = super().authenticate(request)

        request.session['oidc_id_token_expiration'] = access_token_payload['exp']
        request.session['oidc_access_token'] = access_token
        request.session['oidc_user_id'] = str(user.id)
        return user, access_token


class KeycloakScheme(OpenApiAuthenticationExtension):
    target_class = 'umbrella.users.auth.DynamicRealmOIDCAuthentication'
    name = 'keycloakAuth'
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name='Bearer',
            token_prefix=self.target.keyword,
        )
