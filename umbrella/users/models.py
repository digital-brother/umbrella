import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as DjangoGroup
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    NO_REALM = 'no_realm'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    realm = models.CharField(default=NO_REALM, max_length=255)

    def __str__(self):
        return self.username


class Group(DjangoGroup):
    """
    Used instead of native Django Group model. It is treated as the same model as Django Group,
    when working with the ORM, even though they are two separate database tables.
    """
    class Types(models.TextChoices):
        DJANGO = 'django', _('Django')
        Keycloak = 'keycloak', _('Keycloak')

    type = models.CharField(max_length=32, choices=Types.choices, default=Types.DJANGO)

    def __str__(self):
        return self.name

    @classmethod
    def create_keycloak_group_and_tag(cls, group_name):
        from umbrella.contracts.models import Tag
        group = cls.objects.create(name=group_name, type=cls.Types.Keycloak)
        Tag.objects.create(name=group_name, group=group, type=Tag.Types.GROUP)
        return group


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
