from django.contrib import admin

from umbrella.contracts.models import Lease, Node

admin.site.register(Lease)
admin.site.register(Node)
