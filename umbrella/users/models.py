import uuid

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



class User(AbstractUser):
    NO_REALM = 'no_realm'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    realm = models.CharField(default=NO_REALM, max_length=255)

    def __str__(self):
        return self.username


class KeycloakGroup(Group):

    group = models.OneToOneField(Group, on_delete=models.CASCADE, parent_link=True, primary_key=True,)

    def __str__(self):
        return self.name

    @classmethod
    def create_keycloak_group_and_group_and_tag(cls, group_name):
        from umbrella.contracts.models import Tag
        keycloak_group = cls.objects.create(name=group_name)
        user_group = Group.objects.get(id=keycloak_group.id)
        Tag.objects.create(name=group_name, group=user_group, tag_type=Tag.TagTypes.GROUPS)
        return user_group


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
