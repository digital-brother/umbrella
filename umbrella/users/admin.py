from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group as DjangoGroup

from .models import User, Group


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


admin.site.unregister(DjangoGroup)


@admin.register(Group)
class GrpupAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
