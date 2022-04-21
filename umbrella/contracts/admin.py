from django.contrib import admin

from umbrella.contracts.models import Contract, Node, Tag

admin.site.register(Contract)
admin.site.register(Node)
admin.site.register(Tag)
