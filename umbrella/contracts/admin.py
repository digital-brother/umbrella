from django.contrib import admin

from umbrella.contracts.models import Contract, Node, Tag

admin.site.register(Contract)
admin.site.register(Tag)


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'contract', 'type']
