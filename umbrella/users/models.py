import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from rest_framework.authtoken.models import Token





class User(AbstractUser):
    NO_REALM = 'no_realm'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    realm = models.CharField(default=NO_REALM, max_length=255)

    def __str__(self):
        return self.username


class KeycloakGroupManager(models.Manager):

    def create_groups(self, name):

        group = Group.objects.create(name=name)
        keycloak_group = KeycloakGroups(group=group)
        keycloak_group.save()
        Tags = apps.get_model('contracts', 'Tags')
        Tags.objects.create(name=name, user_groups=group, tag_group='groups')

        return group


class KeycloakGroups(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='keycloak_groups',  blank=True, null=True)

    objects = KeycloakGroupManager()

    def __str__(self):
        return self.group.name




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
