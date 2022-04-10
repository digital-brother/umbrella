from django.contrib import admin

from umbrella.contracts.models import Contract, Node

admin.site.register(Contract)
admin.site.register(Node)
