import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
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


@receiver(models.signals.post_save, sender=User)
def tags_created(sender, instance, created, **kwargs):
    user = User.objects.filter(pk=instance.pk).last()
    groups = user.groups.all()
    if groups:
        for group in groups:
            from umbrella.contracts.models import Tags  # TODO Ask Alex about problem with importing models - now import localy
            tag_exist = Tags.objects.filter(name=group).exists()
            if not tag_exist:
                data = {
                    "name": group,
                    'tag_group': 'groups',
                }
                Tags.objects.create(**data)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
