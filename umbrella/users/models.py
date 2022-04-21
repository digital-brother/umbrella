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


class KeycloakGroups(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='keycloak_groups', blank=True, null=True)

    def __str__(self):
        return self.group.name

    @classmethod
    def create_related_object(cls, group_name):
        user_group = Group.objects.create(name=group_name)
        cls.objects.create(group=user_group)
        Tags = apps.get_model('contracts', 'Tags')
        Tags.objects.create(name=group_name, user_groups=user_group, tag_group='groups')

        return user_group


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
