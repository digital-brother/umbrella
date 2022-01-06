"""The file is used to display your models in the Django admin panel."""

from django.contrib import admin

from .models.lease import Lease
from .utils.lease_util import LeaseColumns


class LeaseAdmin(admin.ModelAdmin):
    """Specialised admin view for the Lease model."""

    list_display = LeaseColumns


# Register your models here.
admin.site.register(Lease, LeaseAdmin)
